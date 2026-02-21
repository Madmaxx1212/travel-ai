"""
AI Travel Guardian+ — Pydantic Schemas
Request/response schemas for all API endpoints.
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime


# ── Auth Schemas ──────────────────────────────────────────────

class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., min_length=5)
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    user_id: int
    username: str
    access_token: str

    class Config:
        from_attributes = True


class TokenData(BaseModel):
    user_id: Optional[int] = None
    username: Optional[str] = None


# ── Flight Schemas ────────────────────────────────────────────

class FlightBase(BaseModel):
    flight_number: str
    airline: str
    source: str
    destination: str
    departure_time: str
    arrival_time: str
    duration_mins: int
    price: float
    aircraft_type: Optional[str] = None
    stops: int = 0
    day_of_week: Optional[int] = None
    month: Optional[int] = None
    historical_delay_rate: Optional[float] = None
    historical_ontime_rate: Optional[float] = None
    airline_sentiment_score: Optional[float] = None
    congestion_index: Optional[float] = None


class FlightResponse(FlightBase):
    id: int
    delay_probability: Optional[float] = None
    delay_risk_score: Optional[float] = None
    risk_level: Optional[str] = None
    ccs_score: Optional[float] = None
    rank: Optional[int] = None
    recommended: bool = False
    shap_top3: Optional[List[Dict[str, Any]]] = None

    class Config:
        from_attributes = True


class FlightSearchParams(BaseModel):
    source: str
    destination: str
    date: Optional[str] = None
    budget: str = "medium"
    priority: str = "balanced"


class FlightSearchResponse(BaseModel):
    flights: List[FlightResponse]
    ranked: List[FlightResponse]
    recommended: Optional[FlightResponse] = None


# ── Delay Prediction Schemas ─────────────────────────────────

class DelayPredictionResponse(BaseModel):
    delay_prob: float
    delay_risk_score: float
    risk_level: str
    shap_top3: List[Dict[str, Any]]


# ── Hotel Schemas ─────────────────────────────────────────────

class HotelResponse(BaseModel):
    id: int
    name: str
    city: str
    address: Optional[str] = None
    price_per_night: float
    budget_tier: Optional[str] = None
    rating: Optional[float] = None
    review_count: Optional[int] = None
    distance_centre_km: Optional[float] = None
    amenities: Optional[str] = None
    safety_score: Optional[float] = None
    rank: Optional[int] = None
    recommendation_reason: Optional[str] = None
    highlight: Optional[str] = None
    consideration: Optional[str] = None

    class Config:
        from_attributes = True


# ── Trip Plan Schemas ─────────────────────────────────────────

class TripPlanCreate(BaseModel):
    session_id: str
    source: str
    destination: str
    travel_date: str
    return_date: Optional[str] = None
    num_days: Optional[int] = None
    budget: Optional[str] = "medium"
    priority: Optional[str] = "balanced"
    num_passengers: int = 1


class TripPlanUpdate(BaseModel):
    budget: Optional[str] = None
    priority: Optional[str] = None
    num_days: Optional[int] = None
    num_passengers: Optional[int] = None
    travel_date: Optional[str] = None
    return_date: Optional[str] = None
    selected_flight_id: Optional[int] = None
    selected_hotel_id: Optional[int] = None
    itinerary_json: Optional[str] = None
    food_json: Optional[str] = None
    total_cost_est: Optional[float] = None
    status: Optional[str] = None


class TripPlanResponse(BaseModel):
    id: int
    session_id: str
    source: str
    destination: str
    travel_date: str
    return_date: Optional[str] = None
    num_days: Optional[int] = None
    budget: Optional[str] = None
    priority: Optional[str] = None
    num_passengers: int = 1
    selected_flight_id: Optional[int] = None
    selected_hotel_id: Optional[int] = None
    itinerary_json: Optional[str] = None
    food_json: Optional[str] = None
    total_cost_est: Optional[float] = None
    status: str = "active"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ── Chat Schemas ──────────────────────────────────────────────

class ChatMessage(BaseModel):
    session_id: str
    message: str
    trip_plan_id: Optional[int] = None


class ChatResponse(BaseModel):
    response_text: str
    response_type: str = "text"
    flight_results: Optional[List[FlightResponse]] = None
    risk_warnings: Optional[List[Dict[str, Any]]] = None
    trip_plan: Optional[TripPlanResponse] = None
    recommended_hotels: Optional[List[HotelResponse]] = None
    itinerary: Optional[Dict[str, Any]] = None


# ── Risk Warning Schema ──────────────────────────────────────

class RiskWarning(BaseModel):
    flight_number: str
    warning_type: str  # delay | service | price | connection
    severity: str      # red | amber | blue
    message: str


# ── Health Check Schema ──────────────────────────────────────

class HealthResponse(BaseModel):
    status: str = "ok"
    model_loaded: bool = False
    db: str = "connected"
    groq: str = "unknown"
    faiss: str = "unknown"
