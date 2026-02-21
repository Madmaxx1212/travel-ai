"""AI Travel Guardian+ — Flights API"""

from fastapi import APIRouter, Depends, HTTPException, Query
from database.database import get_db
from database.models import Flight
from database.schemas import FlightSearchResponse, FlightResponse, DelayPredictionResponse

router = APIRouter(prefix="/api/v1/flights", tags=["flights"])


@router.get("/search")
async def search_flights(
    source: str = Query(...), destination: str = Query(...),
    date: str = Query(None), budget: str = Query("medium"),
    priority: str = Query("balanced"), db=Depends(get_db),
):
    """Search and rank flights on a route."""
    from main import delay_predictor
    from ml.ccs_calculator import rank_flights

    source = source.upper()
    destination = destination.upper()

    flights_orm = db.query(Flight).filter(
        Flight.source == source, Flight.destination == destination,
    ).all()

    if not flights_orm:
        return {"flights": [], "ranked": [], "recommended": None}

    # Deduplicate
    seen = set()
    flights_data = []
    for f in flights_orm:
        if f.flight_number not in seen:
            seen.add(f.flight_number)
            flights_data.append({
                "id": f.id, "flight_number": f.flight_number, "airline": f.airline,
                "source": f.source, "destination": f.destination,
                "departure_time": f.departure_time, "arrival_time": f.arrival_time,
                "duration_mins": f.duration_mins, "price": f.price,
                "aircraft_type": f.aircraft_type, "stops": f.stops,
                "day_of_week": f.day_of_week or 3, "month": f.month or 6,
                "historical_delay_rate": f.historical_delay_rate or 0.15,
                "historical_ontime_rate": f.historical_ontime_rate or 0.85,
                "airline_sentiment_score": f.airline_sentiment_score or 0.7,
                "congestion_index": f.congestion_index or 0.5,
            })

    # Predictions
    if delay_predictor and delay_predictor.model:
        flights_data = delay_predictor.predict_batch(flights_data[:20])

    ranked = rank_flights(flights_data, priority, budget)
    recommended = ranked[0] if ranked else None

    return {"flights": flights_data, "ranked": ranked[:5], "recommended": recommended}


@router.get("/{flight_id}")
async def get_flight(flight_id: int, db=Depends(get_db)):
    """Get full flight details with delay prediction."""
    flight = db.query(Flight).filter(Flight.id == flight_id).first()
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")

    data = {
        "id": flight.id, "flight_number": flight.flight_number, "airline": flight.airline,
        "source": flight.source, "destination": flight.destination,
        "departure_time": flight.departure_time, "arrival_time": flight.arrival_time,
        "duration_mins": flight.duration_mins, "price": flight.price,
        "aircraft_type": flight.aircraft_type, "stops": flight.stops,
        "historical_delay_rate": flight.historical_delay_rate,
        "airline_sentiment_score": flight.airline_sentiment_score,
        "congestion_index": flight.congestion_index,
    }

    from main import delay_predictor
    if delay_predictor and delay_predictor.model:
        flight_dict = {**data, "day_of_week": flight.day_of_week or 3, "month": flight.month or 6,
                       "historical_ontime_rate": flight.historical_ontime_rate or 0.85}
        pred = delay_predictor.predict(flight_dict)
        data.update(pred)

    return data


@router.get("/{flight_id}/predict")
async def predict_delay(flight_id: int, db=Depends(get_db)):
    """Get delay prediction for a specific flight."""
    flight = db.query(Flight).filter(Flight.id == flight_id).first()
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")

    from main import delay_predictor
    if not delay_predictor or not delay_predictor.model:
        raise HTTPException(status_code=503, detail="ML model not loaded")

    flight_dict = {
        "departure_time": flight.departure_time, "day_of_week": flight.day_of_week or 3,
        "month": flight.month or 6, "historical_delay_rate": flight.historical_delay_rate or 0.15,
        "historical_ontime_rate": flight.historical_ontime_rate or 0.85,
        "congestion_index": flight.congestion_index or 0.5,
        "duration_mins": flight.duration_mins, "stops": flight.stops,
        "price": flight.price, "airline": flight.airline,
        "source": flight.source, "destination": flight.destination,
    }

    return delay_predictor.predict(flight_dict)
