"""AI Travel Guardian+ — Trips API (CRUD)"""

import json
from fastapi import APIRouter, Depends, HTTPException
from database.database import get_db
from database.models import TripPlan
from database.schemas import TripPlanCreate, TripPlanUpdate, TripPlanResponse

router = APIRouter(prefix="/api/v1/trips", tags=["trips"])


@router.post("/", response_model=TripPlanResponse)
async def create_trip(trip: TripPlanCreate, db=Depends(get_db)):
    db_trip = TripPlan(**trip.model_dump())
    db.add(db_trip)
    db.commit()
    db.refresh(db_trip)
    return db_trip


@router.get("/{trip_plan_id}", response_model=TripPlanResponse)
async def get_trip(trip_plan_id: int, db=Depends(get_db)):
    trip = db.query(TripPlan).filter(TripPlan.id == trip_plan_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip plan not found")
    return trip


@router.put("/{trip_plan_id}", response_model=TripPlanResponse)
async def update_trip(trip_plan_id: int, updates: TripPlanUpdate, db=Depends(get_db)):
    trip = db.query(TripPlan).filter(TripPlan.id == trip_plan_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip plan not found")
    for field, value in updates.model_dump(exclude_none=True).items():
        setattr(trip, field, value)
    db.commit()
    db.refresh(trip)
    return trip


@router.get("/session/{session_id}")
async def get_session_trips(session_id: str, db=Depends(get_db)):
    trips = db.query(TripPlan).filter(TripPlan.session_id == session_id).order_by(TripPlan.created_at.desc()).all()
    return [TripPlanResponse.model_validate(t) for t in trips]
