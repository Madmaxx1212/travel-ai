"""
AI Travel Guardian+ — Replan Agent
Detects user intent to change existing plans and triggers replanning.
"""

from agents.state import TravelState
from llm.prompts import REPLAN_DETECTION_PROMPT


def replan_agent(state: TravelState, llm_client) -> dict:
    """Detect if user wants to modify their trip plan and what changed."""
    user_message = state.get("user_message", "")

    # Build current plan summary
    current_plan = (
        f"Source: {state.get('source', 'N/A')}, "
        f"Destination: {state.get('destination', 'N/A')}, "
        f"Date: {state.get('travel_date', 'N/A')}, "
        f"Days: {state.get('num_days', 'N/A')}, "
        f"Budget: {state.get('budget', 'N/A')}, "
        f"Priority: {state.get('priority', 'N/A')}, "
        f"Passengers: {state.get('num_passengers', 1)}"
    )

    prompt = REPLAN_DETECTION_PROMPT.format(
        user_message=user_message, current_plan=current_plan,
    )
    messages = [
        {"role": "system", "content": "You are a travel plan change detector. Return valid JSON only."},
        {"role": "user", "content": prompt},
    ]

    try:
        result = llm_client.chat_json(messages, model=llm_client.fast_model, temperature=0.1)
    except Exception:
        return {"requires_replanning": False, "replan_change_type": "no_change"}

    if isinstance(result, dict) and "error" not in result:
        requires = result.get("requires_replanning", False)
        change_type = result.get("change_type", "no_change")
        new_values = result.get("new_values", {})
        confirm_msg = result.get("user_friendly_confirm", "")

        updates = {
            "requires_replanning": requires,
            "replan_change_type": change_type,
        }

        if requires and new_values:
            if new_values.get("num_days") is not None:
                updates["num_days"] = new_values["num_days"]
            if new_values.get("budget") is not None:
                updates["budget"] = new_values["budget"]
            if new_values.get("priority") is not None:
                updates["priority"] = new_values["priority"]
            if new_values.get("num_passengers") is not None:
                updates["num_passengers"] = new_values["num_passengers"]
            if new_values.get("travel_date") is not None:
                updates["travel_date"] = new_values["travel_date"]
            if new_values.get("destination") is not None:
                from utils.helpers import normalize_city
                _, iata = normalize_city(new_values["destination"])
                updates["destination"] = iata

            if confirm_msg:
                updates["response_text"] = confirm_msg

        return updates

    return {"requires_replanning": False, "replan_change_type": "no_change"}
