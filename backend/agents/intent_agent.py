"""
AI Travel Guardian+ — Intent Agent
Parses user messages into structured travel intent using Groq LLM.
"""

from agents.state import TravelState
from llm.prompts import INTENT_EXTRACTION_PROMPT
from utils.helpers import normalize_city, parse_date


def intent_agent(state: TravelState, llm_client) -> dict:
    """Extract travel intent from user message using LLM."""
    user_message = state.get("user_message", "")

    prompt = INTENT_EXTRACTION_PROMPT.format(user_message=user_message)
    messages = [
        {"role": "system", "content": "You are a travel intent extraction AI. Always respond with valid JSON only."},
        {"role": "user", "content": prompt},
    ]

    try:
        result = llm_client.chat_json(messages, model=llm_client.fast_model, temperature=0.1)
    except Exception:
        return {
            "needs_clarification": True,
            "clarification_question": "I had trouble understanding your request. Could you tell me your source city, destination, and travel dates?",
            "response_type": "clarification",
            "response_text": "I had trouble understanding your request. Could you tell me your source city, destination, and travel dates?",
        }

    if isinstance(result, dict) and "error" in result:
        return {
            "needs_clarification": True,
            "clarification_question": "Could you please provide more details about your trip? I need at least a destination and travel date.",
            "response_type": "clarification",
            "response_text": "Could you please provide more details about your trip? I need at least a destination and travel date.",
        }

    # Normalize cities
    updates = {}
    source_raw = result.get("source")
    dest_raw = result.get("destination")

    if source_raw:
        city_name, iata = normalize_city(source_raw)
        updates["source"] = iata
    else:
        updates["source"] = state.get("source")

    if dest_raw:
        city_name, iata = normalize_city(dest_raw)
        updates["destination"] = iata
    else:
        updates["destination"] = state.get("destination")

    # Parse dates
    travel_date = result.get("travel_date")
    if travel_date:
        parsed = parse_date(travel_date)
        updates["travel_date"] = parsed or travel_date
    else:
        updates["travel_date"] = state.get("travel_date")

    return_date = result.get("return_date")
    if return_date:
        parsed = parse_date(return_date)
        updates["return_date"] = parsed or return_date

    # Other fields
    updates["num_days"] = result.get("num_days") or state.get("num_days")
    updates["budget"] = result.get("budget") or state.get("budget", "medium")
    updates["priority"] = result.get("priority") or state.get("priority", "balanced")
    updates["num_passengers"] = result.get("num_passengers") or state.get("num_passengers", 1)
    updates["dietary"] = result.get("dietary") or state.get("dietary", "any")
    updates["traveller_type"] = result.get("traveller_type") or state.get("traveller_type", "solo")
    updates["needs_clarification"] = result.get("needs_clarification", False)
    updates["clarification_question"] = result.get("clarification_question")

    if updates["needs_clarification"]:
        question = updates["clarification_question"] or "Could you provide more details about your trip?"
        updates["response_type"] = "clarification"
        updates["response_text"] = question

    return updates
