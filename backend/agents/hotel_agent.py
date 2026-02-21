"""
AI Travel Guardian+ — Hotel Agent
Recommends hotels based on budget, location, and safety scores using DB + LLM.
"""

import json
from agents.state import TravelState
from database.database import SessionLocal
from database.models import Hotel
from llm.prompts import HOTEL_RECOMMENDATION_PROMPT
from utils.helpers import IATA_TO_CITY


def hotel_agent(state: TravelState, llm_client) -> dict:
    """Query hotels and generate personalised recommendations via LLM."""
    destination_iata = state.get("destination", "")
    destination_city = IATA_TO_CITY.get(destination_iata, destination_iata)
    budget = state.get("budget", "medium")
    traveller_type = state.get("traveller_type", "solo")
    priority = state.get("priority", "balanced")
    num_days = state.get("num_days", 3)

    db = SessionLocal()
    try:
        # Query hotels matching city and budget
        budget_tiers = {"budget": ["budget"], "medium": ["budget", "medium"], "luxury": ["medium", "luxury"]}
        tiers = budget_tiers.get(budget, ["budget", "medium"])

        hotels_orm = db.query(Hotel).filter(
            Hotel.city == destination_city,
            Hotel.budget_tier.in_(tiers),
        ).order_by(Hotel.safety_score.desc(), Hotel.rating.desc()).limit(6).all()

        if not hotels_orm:
            # Fallback: try any hotel in that city
            hotels_orm = db.query(Hotel).filter(
                Hotel.city == destination_city
            ).order_by(Hotel.rating.desc()).limit(6).all()

        if not hotels_orm:
            return {"recommended_hotels": []}

        hotels_data = []
        for h in hotels_orm:
            hotels_data.append({
                "id": h.id, "name": h.name, "city": h.city,
                "address": h.address, "price_per_night": h.price_per_night,
                "budget_tier": h.budget_tier, "rating": h.rating,
                "review_count": h.review_count, "distance_centre_km": h.distance_centre_km,
                "amenities": h.amenities, "safety_score": h.safety_score,
            })

        # LLM recommendation
        hotels_summary = json.dumps(hotels_data, indent=2)
        prompt = HOTEL_RECOMMENDATION_PROMPT.format(
            hotels_data=hotels_summary, budget=budget,
            traveller_type=traveller_type, priority=priority,
            destination=destination_city, num_days=num_days,
        )
        messages = [
            {"role": "system", "content": "You are a hotel recommendation AI. Return valid JSON array only."},
            {"role": "user", "content": prompt},
        ]

        try:
            llm_recs = llm_client.chat_json(messages, model=llm_client.fast_model, temperature=0.3)
            if isinstance(llm_recs, list):
                for rec in llm_recs[:3]:
                    hotel_id = rec.get("hotel_id")
                    for hd in hotels_data:
                        if hd["id"] == hotel_id or hd["name"] == rec.get("name"):
                            hd["rank"] = rec.get("rank", 0)
                            hd["recommendation_reason"] = rec.get("recommendation_reason", "")
                            hd["highlight"] = rec.get("highlight", "")
                            hd["consideration"] = rec.get("consideration")
                            break
        except Exception:
            # Fallback: use top 3 by rating
            for i, hd in enumerate(hotels_data[:3]):
                hd["rank"] = i + 1
                hd["recommendation_reason"] = f"Highly rated {hd['budget_tier']} option in {destination_city}."
                hd["highlight"] = f"Rating: {hd['rating']}/5"

        # Return top 3 with recommendations
        recommended = sorted(
            [h for h in hotels_data if h.get("rank")],
            key=lambda x: x.get("rank", 99)
        )[:3]

        if not recommended:
            recommended = hotels_data[:3]
            for i, h in enumerate(recommended):
                h["rank"] = i + 1

        return {"recommended_hotels": recommended}
    finally:
        db.close()
