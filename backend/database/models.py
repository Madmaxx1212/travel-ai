"""
AI Travel Guardian+ — SQLAlchemy ORM Models
All 7 database tables for the application.
"""

from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Text, Float, DateTime,
    ForeignKey, Boolean
)
from database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    preferences = Column(Text, default='{"budget":"medium","priority":"balanced"}')


class Flight(Base):
    __tablename__ = "flights"

    id = Column(Integer, primary_key=True, autoincrement=True)
    flight_number = Column(String(20), nullable=False)
    airline = Column(String(100), nullable=False)
    source = Column(String(10), nullable=False)
    destination = Column(String(10), nullable=False)
    departure_time = Column(String(10), nullable=False)
    arrival_time = Column(String(10), nullable=False)
    duration_mins = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    aircraft_type = Column(String(50))
    stops = Column(Integer, default=0)
    day_of_week = Column(Integer)
    month = Column(Integer)
    historical_delay_rate = Column(Float)
    historical_ontime_rate = Column(Float)
    airline_sentiment_score = Column(Float)
    congestion_index = Column(Float)


class DelayPrediction(Base):
    __tablename__ = "delay_predictions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    flight_id = Column(Integer, ForeignKey("flights.id"))
    prediction_date = Column(String(20), nullable=False)
    delay_prob = Column(Float, nullable=False)
    delay_risk_score = Column(Float, nullable=False)
    shap_json = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class Hotel(Base):
    __tablename__ = "hotels"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    city = Column(String(100), nullable=False)
    address = Column(Text)
    price_per_night = Column(Float, nullable=False)
    budget_tier = Column(String(20))
    rating = Column(Float)
    review_count = Column(Integer)
    distance_centre_km = Column(Float)
    amenities = Column(Text)
    latitude = Column(Float)
    longitude = Column(Float)
    safety_score = Column(Float)


class TripPlan(Base):
    __tablename__ = "trip_plans"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    session_id = Column(String(100), nullable=False)
    source = Column(String(100), nullable=False)
    destination = Column(String(100), nullable=False)
    travel_date = Column(String(20), nullable=False)
    return_date = Column(String(20))
    num_days = Column(Integer)
    budget = Column(String(20))
    priority = Column(String(30))
    num_passengers = Column(Integer, default=1)
    selected_flight_id = Column(Integer, ForeignKey("flights.id"), nullable=True)
    selected_hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=True)
    itinerary_json = Column(Text)
    food_json = Column(Text)
    total_cost_est = Column(Float)
    status = Column(String(20), default="active")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(100), nullable=False)
    trip_plan_id = Column(Integer, ForeignKey("trip_plans.id"), nullable=True)
    role = Column(String(20), nullable=False)
    content = Column(Text, nullable=False)
    message_type = Column(String(30), default="text")
    metadata_json = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class AirlineReview(Base):
    __tablename__ = "airline_reviews"

    id = Column(Integer, primary_key=True, autoincrement=True)
    airline = Column(String(100), nullable=False)
    review_text = Column(Text, nullable=False)
    overall_rating = Column(Float)
    punctuality_score = Column(Float)
    staff_score = Column(Float)
    comfort_score = Column(Float)
    value_score = Column(Float)
    food_score = Column(Float)
    sentiment_label = Column(String(20))
    source = Column(String(50), default="kaggle")
