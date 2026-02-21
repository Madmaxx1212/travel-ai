"""
AI Travel Guardian+ — Explanation Agent
Generates natural language explanations for flight recommendations using SHAP + LLM.
"""

import json
from agents.state import TravelState
from llm.prompts import FLIGHT_EXPLANATION_PROMPT
from ml.shap_explainer import format_shap_explanation


def explanation_agent(state: TravelState, llm_client) -> dict:
    """Generate LLM-powered explanation for the recommended flight."""
    recommended = state.get("recommended_flight")
    if not recommended:
        return {"flight_explanation": "No flight recommendation available to explain."}

    shap_top3 = recommended.get("shap_top3", [])
    shap_text = format_shap_explanation(shap_top3)
    ccs_score = round(recommended.get("ccs_score", 0) * 100, 1)

    flight_summary = json.dumps({
        "flight_number": recommended.get("flight_number"),
        "airline": recommended.get("airline"),
        "source": recommended.get("source"),
        "destination": recommended.get("destination"),
        "departure_time": recommended.get("departure_time"),
        "arrival_time": recommended.get("arrival_time"),
        "duration_mins": recommended.get("duration_mins"),
        "price": recommended.get("price"),
        "stops": recommended.get("stops"),
        "delay_probability": recommended.get("delay_probability"),
        "risk_level": recommended.get("risk_level"),
        "airline_sentiment_score": recommended.get("airline_sentiment_score"),
        "ccs_score": ccs_score,
    }, indent=2)

    prompt = FLIGHT_EXPLANATION_PROMPT.format(
        flight_data=flight_summary,
        shap_explanation=shap_text,
        user_priority=state.get("priority", "balanced"),
        user_budget=state.get("budget", "medium"),
        airline=recommended.get("airline", ""),
        flight_number=recommended.get("flight_number", ""),
        ccs_score=ccs_score,
    )

    messages = [
        {"role": "system", "content": "You are AI Travel Guardian+, a friendly travel assistant. Be concise."},
        {"role": "user", "content": prompt},
    ]

    try:
        explanation = llm_client.chat(messages, model=llm_client.fast_model, temperature=0.4, max_tokens=400)
    except Exception:
        explanation = (
            f"✈️ I recommend **{recommended.get('airline')} {recommended.get('flight_number')}** — "
            f"scoring {ccs_score}/100 on our Convenience Score. {shap_text}"
        )

    return {"flight_explanation": explanation}
