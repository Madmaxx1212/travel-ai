"""AI Travel Guardian+ — Chat API (WebSocket + REST)"""

import json
import uuid
import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from database.database import SessionLocal, get_db
from database.models import Conversation, TripPlan
from database.schemas import ChatMessage, ChatResponse

router = APIRouter(prefix="/api/v1/chat", tags=["chat"])


@router.websocket("/ws/{session_id}")
async def websocket_chat(websocket: WebSocket, session_id: str):
    """WebSocket endpoint for real-time chat."""
    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_json()
            user_message = data.get("message", "")
            trip_plan_id = data.get("trip_plan_id")

            if not user_message:
                await websocket.send_json({"type": "error", "content": "Empty message"})
                continue

            # Save user message
            db = SessionLocal()
            try:
                conv = Conversation(
                    session_id=session_id, role="user",
                    content=user_message, message_type="text",
                    trip_plan_id=trip_plan_id,
                )
                db.add(conv)
                db.commit()

                # Get conversation history
                history = db.query(Conversation).filter(
                    Conversation.session_id == session_id
                ).order_by(Conversation.created_at.desc()).limit(10).all()
                history_list = [{"role": h.role, "content": h.content} for h in reversed(history)]

                # Load existing trip plan state if any
                trip_state = {}
                if trip_plan_id:
                    trip = db.query(TripPlan).filter(TripPlan.id == trip_plan_id).first()
                    if trip:
                        trip_state = {
                            "source": trip.source, "destination": trip.destination,
                            "travel_date": trip.travel_date, "num_days": trip.num_days,
                            "budget": trip.budget, "priority": trip.priority,
                            "num_passengers": trip.num_passengers or 1,
                        }
            finally:
                db.close()

            # Run agent pipeline
            from main import agent_pipeline
            if not agent_pipeline:
                await websocket.send_json({"type": "chunk", "content": "System is initializing. Please try again in a moment."})
                await websocket.send_json({"type": "done", "full_response": "System is initializing."})
                continue

            await websocket.send_json({"type": "chunk", "content": "Analysing your request..."})

            state = {
                "user_message": user_message,
                "session_id": session_id,
                "conversation_history": history_list,
                "num_passengers": 1,
                "dietary": "any",
                "traveller_type": "solo",
                "needs_clarification": False,
                "available_flights": [],
                "ranked_flights": [],
                "risk_warnings": [],
                "recommended_hotels": [],
                "food_recommendations": [],
                "delay_predictions": [],
                "shap_explanations": [],
                "requires_replanning": False,
                "response_text": "",
                "response_type": "general",
                **trip_state,
            }

            result = await asyncio.to_thread(agent_pipeline.run, state)

            # Stream response text
            response_text = result.get("response_text", "")
            chunk_size = 50
            for i in range(0, len(response_text), chunk_size):
                await websocket.send_json({
                    "type": "chunk",
                    "content": response_text[i:i + chunk_size],
                })

            # Send structured data
            if result.get("ranked_flights"):
                await websocket.send_json({
                    "type": "flight_results",
                    "data": result["ranked_flights"][:5],
                })

            if result.get("risk_warnings"):
                await websocket.send_json({
                    "type": "risk_warnings",
                    "data": result["risk_warnings"],
                })

            if result.get("itinerary") or result.get("recommended_hotels"):
                trip_data = {
                    "source": result.get("source"),
                    "destination": result.get("destination"),
                    "travel_date": result.get("travel_date"),
                    "num_days": result.get("num_days"),
                    "budget": result.get("budget"),
                    "recommended_flight": result.get("recommended_flight"),
                    "recommended_hotels": result.get("recommended_hotels", []),
                    "itinerary": result.get("itinerary"),
                    "food_recommendations": result.get("food_recommendations", []),
                }
                await websocket.send_json({"type": "trip_plan", "data": trip_data})

            # Save trip plan
            saved_trip_id = trip_plan_id
            if result.get("response_type") in ("trip_plan", "replan") and result.get("destination"):
                db = SessionLocal()
                try:
                    if trip_plan_id:
                        trip = db.query(TripPlan).filter(TripPlan.id == trip_plan_id).first()
                        if trip:
                            trip.itinerary_json = json.dumps(result.get("itinerary")) if result.get("itinerary") else trip.itinerary_json
                            trip.food_json = json.dumps(result.get("food_recommendations")) if result.get("food_recommendations") else trip.food_json
                            trip.num_days = result.get("num_days") or trip.num_days
                            trip.budget = result.get("budget") or trip.budget
                            db.commit()
                            saved_trip_id = trip.id
                    else:
                        rec_flight = result.get("recommended_flight", {})
                        rec_hotel = result.get("recommended_hotels", [{}])
                        trip = TripPlan(
                            session_id=session_id,
                            source=result.get("source", ""),
                            destination=result.get("destination", ""),
                            travel_date=result.get("travel_date", "TBD"),
                            num_days=result.get("num_days"),
                            budget=result.get("budget", "medium"),
                            priority=result.get("priority", "balanced"),
                            num_passengers=result.get("num_passengers", 1),
                            selected_flight_id=rec_flight.get("id"),
                            selected_hotel_id=rec_hotel[0].get("id") if rec_hotel else None,
                            itinerary_json=json.dumps(result.get("itinerary")) if result.get("itinerary") else None,
                            food_json=json.dumps(result.get("food_recommendations")) if result.get("food_recommendations") else None,
                        )
                        db.add(trip)
                        db.commit()
                        db.refresh(trip)
                        saved_trip_id = trip.id
                finally:
                    db.close()

            # Save assistant message
            db = SessionLocal()
            try:
                conv = Conversation(
                    session_id=session_id, role="assistant",
                    content=response_text,
                    message_type=result.get("response_type", "text"),
                    trip_plan_id=saved_trip_id,
                    metadata_json=json.dumps({
                        "flight_count": len(result.get("ranked_flights", [])),
                        "warning_count": len(result.get("risk_warnings", [])),
                    }),
                )
                db.add(conv)
                db.commit()
            finally:
                db.close()

            await websocket.send_json({
                "type": "done",
                "full_response": response_text,
                "trip_plan_id": saved_trip_id,
                "response_type": result.get("response_type", "general"),
            })

    except WebSocketDisconnect:
        pass
    except Exception as e:
        try:
            await websocket.send_json({"type": "error", "content": str(e)[:200]})
        except Exception:
            pass


@router.post("/message", response_model=ChatResponse)
async def chat_message(msg: ChatMessage, db=Depends(get_db)):
    """Non-streaming REST chat endpoint (fallback)."""
    from main import agent_pipeline

    if not agent_pipeline:
        return ChatResponse(
            response_text="System is initializing. Please try again.",
            response_type="general",
        )

    # Get history
    history = db.query(Conversation).filter(
        Conversation.session_id == msg.session_id
    ).order_by(Conversation.created_at.desc()).limit(10).all()
    history_list = [{"role": h.role, "content": h.content} for h in reversed(history)]

    # Save user message
    db.add(Conversation(
        session_id=msg.session_id, role="user",
        content=msg.message, message_type="text",
        trip_plan_id=msg.trip_plan_id,
    ))
    db.commit()

    state = {
        "user_message": msg.message,
        "session_id": msg.session_id,
        "conversation_history": history_list,
        "num_passengers": 1, "dietary": "any", "traveller_type": "solo",
        "needs_clarification": False,
        "available_flights": [], "ranked_flights": [],
        "risk_warnings": [], "recommended_hotels": [],
        "food_recommendations": [], "delay_predictions": [],
        "shap_explanations": [], "requires_replanning": False,
        "response_text": "", "response_type": "general",
    }

    result = agent_pipeline.run(state)

    # Save assistant message
    db.add(Conversation(
        session_id=msg.session_id, role="assistant",
        content=result.get("response_text", ""),
        message_type=result.get("response_type", "text"),
    ))
    db.commit()

    return ChatResponse(
        response_text=result.get("response_text", ""),
        response_type=result.get("response_type", "general"),
        flight_results=result.get("ranked_flights"),
        risk_warnings=result.get("risk_warnings"),
        itinerary=result.get("itinerary"),
    )
