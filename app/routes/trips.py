from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List
import io

from app.database import get_db
from app.models import DBTrip, DBVehicle, DBDriver
from app.schemas import TripCreate, TripResponse
from app.dependencies import get_current_user_role

router = APIRouter(prefix="/trips", tags=["Trips"])

# 1. POST Route: Log trip (ALL ROLES)
@router.post("", response_model=TripResponse)
def log_trip(trip: TripCreate, db: Session = Depends(get_db), role: str = Depends(get_current_user_role)):
    vehicle_exists = db.query(DBVehicle).filter(DBVehicle.id == trip.vehicle_id).first()
    if not vehicle_exists: raise HTTPException(status_code=404, detail="Vehicle not found")
    driver_exists = db.query(DBDriver).filter(DBDriver.id == trip.driver_id).first()
    if not driver_exists: raise HTTPException(status_code=404, detail="Driver not found")

    new_trip = DBTrip(vehicle_id=trip.vehicle_id, driver_id=trip.driver_id, start_location=trip.start_location, end_location=trip.end_location, distance_km=trip.distance_km, fuel_used_liters=trip.fuel_used_liters)
    db.add(new_trip)
    db.commit()
    db.refresh(new_trip)
    return new_trip

# 2. GET Route: Fetch all trips (ALL ROLES)
@router.get("", response_model=List[TripResponse])
def get_trips(db: Session = Depends(get_db), role: str = Depends(get_current_user_role)):
    return db.query(DBTrip).all()

# 3. EXPORT Route: Generate CSV Spreadsheet (MANAGER ONLY)
@router.get("/export/csv")
def export_trips_csv(db: Session = Depends(get_db), role: str = Depends(get_current_user_role)):
    if role != "manager":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied: Managers only")

    trips = db.query(DBTrip).all()
    
    # Initialize an in-memory text stream
    output = io.StringIO()
    # Write the CSV column headers
    output.write("Trip ID,Vehicle ID,Driver ID,Start Location,End Location,Distance (KM),Fuel Used (Liters)\n")
    
    # Populate data rows
    for t in trips:
        output.write(f"{t.id},{t.vehicle_id},{t.driver_id},{t.start_location},{t.end_location},{t.distance_km},{t.fuel_used_liters}\n")
    
    # Reset text stream pointer
    output.seek(0)
    
    # Return as a downloadable spreadsheet file attachment
    return StreamingResponse(
        io.BytesIO(output.getvalue().encode("utf-8")),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=fleet_trips_report.csv"}
    )

