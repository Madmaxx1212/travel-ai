"""
AI Travel Guardian+ — FastAPI Application Entry Point
Initializes database, ML models, FAISS indices, and all API routes.
"""

import json
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from utils.logger import logger

# Global state
app_state = {}
delay_predictor = None
agent_pipeline = None
rag_retriever = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown lifecycle."""
    global delay_predictor, agent_pipeline, rag_retriever

    logger.info("=" * 60)
    logger.info("  AI Travel Guardian+ — Starting Up")
    logger.info("=" * 60)

    # 1. Initialize database
    try:
        from database.database import init_db, engine
        init_db()
        logger.info("[OK] Database tables created")
        app_state["db"] = "connected"
    except Exception as e:
        logger.error(f"[ERROR] Database init failed: {e}")

    # 2. Seed data if empty
    try:
        from database.database import SessionLocal
        from database.models import Flight
        db = SessionLocal()
        flight_count = db.query(Flight).count()
        db.close()
        if flight_count == 0:
            logger.info("[INFO] Database empty -- running seed data...")
            from database.seed_data import seed_database
            seed_database()
    except Exception as e:
        logger.error(f"[ERROR] Seed data failed: {e}")

    # 3. Train/load ML model
    try:
        from ml.delay_predictor import FlightDelayPredictor
        predictor = FlightDelayPredictor()
        if predictor.model is None:
            logger.info("[INFO] Training XGBoost model...")
            import pandas as pd
            data_dir = Path(__file__).resolve().parent.parent / "data"
            csv_path = data_dir / "sample_flights.csv"
            if csv_path.exists():
                df = pd.read_csv(csv_path)
                metrics = predictor.train(df)
                logger.info(f"[OK] Model trained -- Accuracy: {metrics['accuracy']}, AUC: {metrics['roc_auc']}")
            else:
                logger.warning("[WARN] No flight data CSV found for training")
        else:
            logger.info("[OK] ML model loaded from disk")
        delay_predictor = predictor
        app_state["model_loaded"] = True
    except Exception as e:
        logger.error(f"[ERROR] ML model failed: {e}")
        app_state["model_loaded"] = False

    # 4. Build FAISS indices
    try:
        from rag.retriever import RAGRetriever
        retriever = RAGRetriever()

        data_dir = Path(__file__).resolve().parent.parent / "data"
        faiss_dir = data_dir / "faiss"
        faiss_dir.mkdir(parents=True, exist_ok=True)

        # Load data for embedding
        from database.database import SessionLocal
        from database.models import Flight, Hotel
        db = SessionLocal()
        flights_orm = db.query(Flight).limit(200).all()
        hotels_orm = db.query(Hotel).all()
        db.close()

        flights_data = [{"flight_number": f.flight_number, "airline": f.airline,
                         "source": f.source, "destination": f.destination,
                         "departure_time": f.departure_time, "arrival_time": f.arrival_time,
                         "duration_mins": f.duration_mins, "price": f.price,
                         "historical_ontime_rate": f.historical_ontime_rate or 0.85,
                         "airline_sentiment_score": f.airline_sentiment_score or 0.7,
                         "stops": f.stops} for f in flights_orm]

        hotels_data = [{"name": h.name, "city": h.city, "price_per_night": h.price_per_night,
                        "budget_tier": h.budget_tier, "rating": h.rating,
                        "distance_centre_km": h.distance_centre_km, "address": h.address or ""}
                       for h in hotels_orm]

        city_data = {}
        knowledge_path = data_dir / "city_knowledge.json"
        if knowledge_path.exists():
            with open(knowledge_path, "r", encoding="utf-8") as f:
                city_data = json.load(f)

        retriever.initialize(
            flights=flights_data, hotels=hotels_data, city_data=city_data,
            faiss_flights_path=str(faiss_dir / "flights"),
            faiss_hotels_path=str(faiss_dir / "hotels"),
            faiss_city_path=str(faiss_dir / "city"),
        )
        rag_retriever = retriever
        logger.info("[OK] FAISS indices built/loaded")
        app_state["faiss_status"] = "ok"
    except Exception as e:
        logger.error(f"[ERROR] FAISS init failed: {e}")
        app_state["faiss_status"] = "error"

    # 5. Initialize Groq LLM + Agent Pipeline
    try:
        from llm.groq_client import GroqLLMClient
        from agents.graph import TravelAgentPipeline

        llm_client = GroqLLMClient(
            api_key=settings.GROQ_API_KEY,
            model=settings.GROQ_MODEL,
            smart_model=settings.GROQ_SMART_MODEL,
        )

        if settings.GROQ_API_KEY != "your_groq_api_key_here":
            connected = llm_client.test_connection()
            app_state["groq_status"] = "ok" if connected else "error"
            logger.info(f"{'[OK]' if connected else '[ERROR]'} Groq API {'connected' if connected else 'failed'}")
        else:
            app_state["groq_status"] = "no_key"
            logger.warning("[WARN] No Groq API key configured -- LLM features disabled")

        agent_pipeline = TravelAgentPipeline(
            llm_client=llm_client,
            delay_predictor=delay_predictor,
            rag_retriever=rag_retriever,
        )
        logger.info("[OK] Agent pipeline initialized")
    except Exception as e:
        logger.error(f"[ERROR] Agent pipeline init failed: {e}")

    logger.info("=" * 60)
    logger.info("  AI Travel Guardian+ — Ready!")
    logger.info(f"  DB: {app_state.get('db', 'unknown')}")
    logger.info(f"  Model: {'loaded' if app_state.get('model_loaded') else 'not loaded'}")
    logger.info(f"  Groq: {app_state.get('groq_status', 'unknown')}")
    logger.info(f"  FAISS: {app_state.get('faiss_status', 'unknown')}")
    logger.info("=" * 60)

    yield  # App is running

    # Shutdown
    logger.info("AI Travel Guardian+ shutting down...")


# Create FastAPI app
app = FastAPI(
    title="AI Travel Guardian+",
    description="LLM + ML powered intelligent travel planning system",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
from api.health import router as health_router
from api.auth import router as auth_router
from api.flights import router as flights_router
from api.chat import router as chat_router
from api.trips import router as trips_router

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(flights_router)
app.include_router(chat_router)
app.include_router(trips_router)


@app.get("/")
async def root():
    return {"message": "AI Travel Guardian+ API", "docs": "/docs", "health": "/api/v1/health"}
