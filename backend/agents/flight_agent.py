"""
AI Travel Guardian+ — Flight Agent
Searches, scores, and ranks flights using delay prediction + CCS.
"""

from agents.state import TravelState
from database.database import SessionLocal
from database.models import Flight
from ml.delay_predictor import FlightDelayPredictor
from ml.ccs_calculator import rank_flights


def flight_agent(state: TravelState, delay_predictor: FlightDelayPredictor) -> dict:
    """Search flights and rank them using ML predictions + CCS."""
    source = state.get("source")
    destination = state.get("destination")
    priority = state.get("priority", "balanced")
    budget = state.get("budget", "medium")

    if not source or not destination:
        return {"available_flights": [], "ranked_flights": [], "recommended_flight": None}

    db = SessionLocal()
    try:
        query = db.query(Flight).filter(
            Flight.source == source,
            Flight.destination == destination,
        )

        # Filter by stops preference
        if budget == "budget":
            query = query.filter(Flight.stops <= 1)
        else:
            query = query.filter(Flight.stops <= 1)

        flights_orm = query.all()

        if not flights_orm:
            return {
                "available_flights": [],
                "ranked_flights": [],
                "recommended_flight": None,
                "response_text": f"Sorry, I couldn't find any flights from {source} to {destination}. Try a different route?",
                "response_type": "general",
            }

        # Deduplicate by flight_number (take first occurrence)
        seen = set()
        unique_flights = []
        for f in flights_orm:
            if f.flight_number not in seen:
                seen.add(f.flight_number)
                unique_flights.append(f)

        # Convert to dicts
        flights_data = []
        for f in unique_flights[:20]:  # Limit to 20 for processing
            flights_data.append({
                "id": f.id,
                "flight_number": f.flight_number,
                "airline": f.airline,
                "source": f.source,
                "destination": f.destination,
                "departure_time": f.departure_time,
                "arrival_time": f.arrival_time,
                "duration_mins": f.duration_mins,
                "price": f.price,
                "aircraft_type": f.aircraft_type,
                "stops": f.stops,
                "day_of_week": f.day_of_week or 3,
                "month": f.month or 6,
                "historical_delay_rate": f.historical_delay_rate or 0.15,
                "historical_ontime_rate": f.historical_ontime_rate or 0.85,
                "airline_sentiment_score": f.airline_sentiment_score or 0.7,
                "congestion_index": f.congestion_index or 0.5,
            })

        # Run delay predictions
        flights_with_predictions = delay_predictor.predict_batch(flights_data)

        # Rank with CCS
        ranked = rank_flights(flights_with_predictions, priority, budget)

        # Take top 5
        top5 = ranked[:5]
        recommended = top5[0] if top5 else None

        return {
            "available_flights": flights_data,
            "ranked_flights": top5,
            "recommended_flight": recommended,
            "delay_predictions": [{
                "flight_number": f.get("flight_number"),
                "delay_probability": f.get("delay_probability"),
                "risk_level": f.get("risk_level"),
            } for f in top5],
            "shap_explanations": [{
                "flight_number": f.get("flight_number"),
                "shap_top3": f.get("shap_top3", []),
            } for f in top5],
        }
    finally:
        db.close()
