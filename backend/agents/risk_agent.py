"""
AI Travel Guardian+ — Risk Agent
Generates warnings for risky flights based on rules and LLM analysis.
"""

import json
from agents.state import TravelState
from llm.prompts import RISK_WARNING_PROMPT


def risk_agent(state: TravelState, llm_client) -> dict:
    """Generate rule-based + LLM-powered risk warnings for ranked flights."""
    ranked_flights = state.get("ranked_flights", [])
    if not ranked_flights:
        return {"risk_warnings": []}

    # ── Rule-based warnings ──
    warnings = []
    prices = [f.get("price", 0) for f in ranked_flights]
    avg_price = sum(prices) / len(prices) if prices else 0

    for f in ranked_flights:
        fn = f.get("flight_number", "N/A")
        delay_prob = f.get("delay_probability", 0)
        sentiment = f.get("airline_sentiment_score", 0.7)
        price = f.get("price", 0)

        if delay_prob > 0.40:
            warnings.append({
                "flight_number": fn, "warning_type": "delay", "severity": "red",
                "message": f"High delay risk ({delay_prob:.0%}). This flight has significant historical delays at this time."
            })
        elif delay_prob > 0.25:
            warnings.append({
                "flight_number": fn, "warning_type": "delay", "severity": "amber",
                "message": f"Moderate delay risk ({delay_prob:.0%}). Consider earlier departure times for better punctuality."
            })

        if sentiment < 0.45:
            warnings.append({
                "flight_number": fn, "warning_type": "service", "severity": "amber",
                "message": f"Below-average service quality. Recent passenger reviews indicate concerns about this airline."
            })

        if avg_price > 0 and price < avg_price * 0.65:
            warnings.append({
                "flight_number": fn, "warning_type": "price", "severity": "blue",
                "message": f"Price significantly below route average (₹{price:.0f} vs avg ₹{avg_price:.0f}). Verify inclusions."
            })

    # ── LLM-based warnings (supplement) ──
    try:
        flights_summary = json.dumps([{
            "flight_number": f.get("flight_number"),
            "airline": f.get("airline"),
            "delay_probability": f.get("delay_probability"),
            "airline_sentiment_score": f.get("airline_sentiment_score"),
            "price": f.get("price"),
            "stops": f.get("stops"),
            "duration_mins": f.get("duration_mins"),
        } for f in ranked_flights], indent=2)

        prompt = RISK_WARNING_PROMPT.format(flights_data=flights_summary)
        messages = [
            {"role": "system", "content": "You are a flight risk analysis AI. Return valid JSON only."},
            {"role": "user", "content": prompt},
        ]
        llm_warnings = llm_client.chat_json(messages, model=llm_client.fast_model, temperature=0.1)

        if isinstance(llm_warnings, list):
            # Merge, deduplicate
            existing_keys = {(w["flight_number"], w["warning_type"]) for w in warnings}
            for lw in llm_warnings:
                key = (lw.get("flight_number"), lw.get("warning_type"))
                if key not in existing_keys:
                    warnings.append(lw)
    except Exception:
        pass  # Rule-based warnings are sufficient

    return {"risk_warnings": warnings}
