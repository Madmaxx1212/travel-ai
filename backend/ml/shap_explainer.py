"""
AI Travel Guardian+ — SHAP Explainer Wrapper
Converts SHAP values into human-readable explanations.
"""

from typing import List, Dict


# Human-readable feature descriptions for explanations
FEATURE_DESCRIPTIONS = {
    "Departure Time": {
        "increases delay risk": "flights departing at this time have historically higher delays",
        "decreases delay risk": "this departure time slot has fewer recorded delays",
    },
    "Day of Week": {
        "increases delay risk": "this day of the week tends to have more flight delays",
        "decreases delay risk": "flights on this day are generally more punctual",
    },
    "Month": {
        "increases delay risk": "this month has historically higher delay rates due to weather/traffic",
        "decreases delay risk": "this is a relatively smooth month for air travel",
    },
    "Weekend Travel": {
        "increases delay risk": "weekend flights often see higher congestion and delays",
        "decreases delay risk": "weekday travel tends to be more punctual",
    },
    "Holiday Period": {
        "increases delay risk": "holiday periods bring increased air traffic and delays",
        "decreases delay risk": "non-holiday period means less congestion",
    },
    "Historical Delay Rate": {
        "increases delay risk": "this flight has a history of delays on this route",
        "decreases delay risk": "this flight has a strong on-time track record",
    },
    "Airport Congestion": {
        "increases delay risk": "the airport is typically congested at this time",
        "decreases delay risk": "low airport congestion at this departure time",
    },
    "Flight Duration": {
        "increases delay risk": "longer flights have more chances of encountering delays",
        "decreases delay risk": "shorter flight routes tend to be more reliable",
    },
    "Number of Stops": {
        "increases delay risk": "connecting flights carry additional delay risk at each stop",
        "decreases delay risk": "direct flights avoid connection-related delays",
    },
    "Price Level": {
        "increases delay risk": "lower-priced flights may indicate less reliable scheduling",
        "decreases delay risk": "premium pricing often correlates with better punctuality",
    },
    "Airline": {
        "increases delay risk": "this airline has a mixed punctuality record",
        "decreases delay risk": "this airline has a strong on-time performance",
    },
    "Departure Airport": {
        "increases delay risk": "this airport has higher average delay rates",
        "decreases delay risk": "this airport handles departures efficiently",
    },
    "Arrival Airport": {
        "increases delay risk": "the destination airport has congestion issues",
        "decreases delay risk": "the arrival airport is well-managed",
    },
}


def format_shap_explanation(shap_top3: List[Dict]) -> str:
    """Convert SHAP top-3 features into a readable paragraph."""
    if not shap_top3:
        return "No detailed explanation available for this prediction."

    parts = []
    for i, item in enumerate(shap_top3):
        feature = item.get("feature", "Unknown")
        direction = item.get("direction", "unknown")
        desc = FEATURE_DESCRIPTIONS.get(feature, {}).get(direction, direction)
        impact = item.get("impact", 0)

        strength = "slightly" if impact < 0.05 else "moderately" if impact < 0.15 else "significantly"
        parts.append(f"**{feature}** {strength} {desc}")

    if len(parts) == 1:
        return f"The main factor is: {parts[0]}."
    elif len(parts) == 2:
        return f"Two key factors: {parts[0]}, and {parts[1]}."
    else:
        return f"Three key factors: {parts[0]}; {parts[1]}; and {parts[2]}."


def shap_to_risk_summary(shap_top3: List[Dict], risk_level: str) -> str:
    """Generate a concise risk summary from SHAP values."""
    risk_emoji = {"low": "🟢", "medium": "🟡", "high": "🟠", "very_high": "🔴"}.get(risk_level, "⚪")
    explanation = format_shap_explanation(shap_top3)
    return f"{risk_emoji} Risk Level: **{risk_level.replace('_', ' ').title()}** — {explanation}"
