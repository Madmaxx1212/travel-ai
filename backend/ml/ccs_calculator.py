"""
AI Travel Guardian+ — Customer Convenience Score (CCS) Calculator
Weighted scoring formula that ranks flights based on user priorities.
"""

from typing import List, Dict


# Priority weight presets
PRIORITY_WEIGHTS = {
    "low_delay":    {"w1": 0.60, "w2": 0.25, "w3": 0.15},
    "low_price":    {"w1": 0.20, "w2": 0.20, "w3": 0.60},
    "best_service": {"w1": 0.25, "w2": 0.60, "w3": 0.15},
    "balanced":     {"w1": 0.34, "w2": 0.33, "w3": 0.33},
}


def calculate_ccs(flight: dict, user_priority: str = "balanced", budget: str = "medium") -> float:
    """
    Calculate Customer Convenience Score for a flight.
    
    CCS = w1 × (1 - delay_risk_score/100) + w2 × airline_sentiment_score + w3 × (1 - price_normalised)
    
    Returns float 0.0-1.0, rounded to 4 decimal places.
    """
    weights = PRIORITY_WEIGHTS.get(user_priority, PRIORITY_WEIGHTS["balanced"])

    delay_risk = flight.get("delay_risk_score", 20) / 100.0
    sentiment = flight.get("airline_sentiment_score", 0.5)
    price_norm = flight.get("price_normalised", 0.5)

    ccs = (
        weights["w1"] * (1 - delay_risk)
        + weights["w2"] * sentiment
        + weights["w3"] * (1 - price_norm)
    )

    return round(max(0.0, min(1.0, ccs)), 4)


def rank_flights(flights: List[dict], user_priority: str = "balanced", budget: str = "medium") -> List[dict]:
    """
    Score all flights with CCS and return sorted list (best first).
    Adds ccs_score, rank, and recommended fields to each flight dict.
    """
    if not flights:
        return []

    # Calculate price_normalised across the batch
    prices = [f.get("price", 0) for f in flights]
    max_price = max(prices) if prices else 1
    if max_price == 0:
        max_price = 1

    for f in flights:
        f["price_normalised"] = round(f.get("price", 0) / max_price, 4)

    # Score each flight
    for f in flights:
        f["ccs_score"] = calculate_ccs(f, user_priority, budget)

    # Sort by CCS descending
    ranked = sorted(flights, key=lambda x: x["ccs_score"], reverse=True)

    # Add rank and recommended flag
    for i, f in enumerate(ranked):
        f["rank"] = i + 1
        f["recommended"] = (i == 0)

    return ranked
