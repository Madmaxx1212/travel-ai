"""
AI Travel Guardian+ — Itinerary Agent
Generates day-wise trip itinerary + food recommendations using city knowledge + LLM.
"""

import json
from pathlib import Path
from agents.state import TravelState
from llm.prompts import ITINERARY_GENERATION_PROMPT
from utils.helpers import IATA_TO_CITY


def itinerary_agent(state: TravelState, llm_client) -> dict:
    """Generate a day-wise itinerary using city knowledge base + LLM."""
    destination_iata = state.get("destination", "")
    destination_city = IATA_TO_CITY.get(destination_iata, destination_iata)
    num_days = state.get("num_days", 3)
    budget = state.get("budget", "medium")
    traveller_type = state.get("traveller_type", "solo")
    dietary = state.get("dietary", "any")

    # Load city knowledge
    data_dir = Path(__file__).resolve().parent.parent.parent / "data"
    knowledge_path = data_dir / "city_knowledge.json"
    city_knowledge = {}

    if knowledge_path.exists():
        with open(knowledge_path, "r", encoding="utf-8") as f:
            all_knowledge = json.load(f)
            city_knowledge = all_knowledge.get(destination_city, {})

    if not city_knowledge:
        city_knowledge_str = f"General knowledge about {destination_city}. Popular tourist destination in India."
    else:
        city_knowledge_str = json.dumps(city_knowledge, indent=2)[:3000]

    prompt = ITINERARY_GENERATION_PROMPT.format(
        destination=destination_city, num_days=num_days,
        traveller_type=traveller_type, budget=budget,
        dietary=dietary, city_knowledge=city_knowledge_str,
    )

    messages = [
        {"role": "system", "content": "You are a travel itinerary planner. Return valid JSON only."},
        {"role": "user", "content": prompt},
    ]

    try:
        result = llm_client.chat_json(messages, model=llm_client.smart_model, temperature=0.5, max_tokens=3000)
    except Exception:
        result = _fallback_itinerary(destination_city, num_days, city_knowledge)

    if isinstance(result, dict) and "error" in result:
        result = _fallback_itinerary(destination_city, num_days, city_knowledge)

    # Extract food recommendations
    food_recs = []
    if isinstance(result, dict) and "days" in result:
        for day in result["days"]:
            for meal in day.get("meals", []):
                meal["day"] = day.get("day", 0)
                food_recs.append(meal)

    return {
        "itinerary": result,
        "food_recommendations": food_recs,
    }


def _fallback_itinerary(city: str, num_days: int, knowledge: dict) -> dict:
    """Generate a basic itinerary from city knowledge without LLM."""
    days = []
    attractions = knowledge.get("top_attractions", [])
    food_spots = knowledge.get("food_spots", [])

    for d in range(1, num_days + 1):
        day_activities = []
        day_meals = []

        # Pick 2-3 attractions per day
        start_idx = (d - 1) * 3
        for i, attr in enumerate(attractions[start_idx:start_idx + 3]):
            times = ["10:00", "14:00", "17:00"]
            day_activities.append({
                "time": times[i] if i < len(times) else "15:00",
                "name": attr["name"],
                "type": "sightseeing",
                "duration_mins": attr.get("duration_mins", 90),
                "description": attr.get("description", ""),
                "cost_estimate": attr.get("cost", "Free"),
                "tips": attr.get("best_time", ""),
            })

        # Pick 1-2 food spots per day
        food_idx = (d - 1) * 2
        for fs in food_spots[food_idx:food_idx + 2]:
            day_meals.append({
                "type": "lunch" if len(day_meals) == 0 else "dinner",
                "name": fs["name"],
                "cuisine": fs["cuisine"],
                "area": fs["area"],
                "price_range": fs["price_range"],
                "must_try": fs["specialty"],
            })

        theme = "Arrival & Exploration" if d == 1 else ("Departure Day" if d == num_days else f"Day {d} Adventures")
        days.append({"day": d, "theme": theme, "activities": day_activities, "meals": day_meals})

    return {"days": days}
