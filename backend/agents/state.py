"""
AI Travel Guardian+ — LangGraph Shared State
TypedDict definition for the multi-agent pipeline state.
"""

from typing import TypedDict, Optional, List, Dict, Any


class TravelState(TypedDict, total=False):
    """Shared state passed between all agents in the LangGraph pipeline."""

    # Input
    user_message: str
    session_id: str
    conversation_history: List[Dict]

    # Extracted intent
    source: Optional[str]
    destination: Optional[str]
    travel_date: Optional[str]
    return_date: Optional[str]
    num_days: Optional[int]
    budget: Optional[str]
    priority: Optional[str]
    num_passengers: int
    dietary: str
    traveller_type: str
    needs_clarification: bool
    clarification_question: Optional[str]

    # Flight results
    available_flights: List[Dict]
    ranked_flights: List[Dict]
    recommended_flight: Optional[Dict]
    risk_warnings: List[Dict]
    flight_explanation: Optional[str]

    # ML predictions
    delay_predictions: List[Dict]
    shap_explanations: List[Dict]

    # Trip components
    recommended_hotels: List[Dict]
    itinerary: Optional[Dict]
    food_recommendations: List[Dict]

    # Replanning
    requires_replanning: bool
    replan_change_type: Optional[str]

    # Final output
    response_text: str
    response_type: str  # clarification|flight_results|trip_plan|general|replan
    trip_plan_id: Optional[int]
    error: Optional[str]
