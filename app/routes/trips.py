from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import DBTrip, DBVehicle, DBDriver
from app.schemas import TripCreate, TripResponse

router = APIRouter(prefix="/trips", tags=["Trips"])

# 1. POST Route: Log a new trip
@router.post("", response_model=TripResponse)
def log_trip(trip: TripCreate, db: Session = Depends(get_db)):
    # Integrity Check: Make sure the vehicle exists
    vehicle_exists = db.query(DBVehicle).filter(DBVehicle.id == trip.vehicle_id).first()
    if not vehicle_exists:
        raise HTTPException(status_code=404, detail="Vehicle not found")
        
    # Integrity Check: Make sure the driver exists
    driver_exists = db.query(DBDriver).filter(DBDriver.id == trip.driver_id).first()
    if not driver_exists:
        raise HTTPException(status_code=404, detail="Driver not found")

    new_trip = DBTrip(
        vehicle_id=trip.vehicle_id,
        driver_id=trip.driver_id,
        start_location=trip.start_location,
        end_location=trip.end_location,
        distance_km=trip.distance_km,
        fuel_used_liters=trip.fuel_used_liters
    )
    db.add(new_trip)
    db.commit()
    db.refresh(new_trip)
    return new_trip

# 2. GET Route: Fetch all trips
@router.get("", response_model=List[TripResponse])
def get_trips(db: Session = Depends(get_db)):
    return db.query(DBTrip).all()

