from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import DBVehicle
from app.schemas import VehicleCreate, VehicleResponse

router = APIRouter(prefix="/vehicles", tags=["Vehicles"])

# 1. POST Route: Add a vehicle
@router.post("", response_model=VehicleResponse)
def add_vehicle(vehicle: VehicleCreate, db: Session = Depends(get_db)):
    db_vehicle = db.query(DBVehicle).filter(DBVehicle.license_plate == vehicle.license_plate).first()
    if db_vehicle:
        raise HTTPException(status_code=400, detail="License plate already registered")
    
    new_vehicle = DBVehicle(
        make=vehicle.make,
        model=vehicle.model,
        year=vehicle.year,
        license_plate=vehicle.license_plate
    )
    db.add(new_vehicle)
    db.commit()
    db.refresh(new_vehicle)
    return new_vehicle

# 2. GET Route: Fetch all vehicles
@router.get("", response_model=List[VehicleResponse])
def get_vehicles(db: Session = Depends(get_db)):
    vehicles = db.query(DBVehicle).all()
    return vehicles

# Keep your existing code at the top, append this to the very bottom:
from app.models import DBTrip
from app.schemas import TripResponse

# 1. Analytical Route: Fetch all trips for a specific vehicle ID
@router.get("/{vehicle_id}/trips", response_model=List[TripResponse])
def get_vehicle_trips(vehicle_id: int, db: Session = Depends(get_db)):
    # Verify vehicle exists first
    vehicle = db.query(DBVehicle).filter(DBVehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
        
    trips = db.query(DBTrip).filter(DBTrip.vehicle_id == vehicle_id).all()
    return trips

# 2. Analytical Route: Calculate fuel efficiency metrics for a vehicle
@router.get("/{vehicle_id}/efficiency")
def get_vehicle_efficiency(vehicle_id: int, db: Session = Depends(get_db)):
    vehicle = db.query(DBVehicle).filter(DBVehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    trips = db.query(DBTrip).filter(DBTrip.vehicle_id == vehicle_id).all()
    if not trips:
        return {
            "vehicle_id": vehicle_id,
            "message": "No trips logged for this vehicle yet.",
            "total_distance_km": 0.0,
            "average_liters_per_100km": 0.0
        }

    # Calculate sums
    total_distance = sum(t.distance_km for t in trips)
    total_fuel = sum(t.fuel_used_liters for t in trips)

    # Prevent division by zero if distance is 0
    avg_efficiency = (total_fuel / total_distance) * 100 if total_distance > 0 else 0.0

    return {
        "vehicle_id": vehicle_id,
        "vehicle_name": f"{vehicle.make} {vehicle.model}",
        "total_trips": len(trips),
        "total_distance_km": round(total_distance, 2),
        "total_fuel_used_liters": round(total_fuel, 2),
        "average_liters_per_100km": round(avg_efficiency, 2)
    }

# Keep your existing code at the top, append this to the very bottom:

# 3. PUT Route: Update an existing vehicle's details
@router.put("/{vehicle_id}", response_model=VehicleResponse)
def update_vehicle(vehicle_id: int, updated_vehicle: VehicleCreate, db: Session = Depends(get_db)):
    db_vehicle = db.query(DBVehicle).filter(DBVehicle.id == vehicle_id).first()
    if not db_vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
        
    # Check if they are trying to change to a license plate that someone else owns
    plate_check = db.query(DBVehicle).filter(
        DBVehicle.license_plate == updated_vehicle.license_plate, 
        DBVehicle.id != vehicle_id
    ).first()
    if plate_check:
        raise HTTPException(status_code=400, detail="License plate already in use by another vehicle")

    db_vehicle.make = updated_vehicle.make
    db_vehicle.model = updated_vehicle.model
    db_vehicle.year = updated_vehicle.year
    db_vehicle.license_plate = updated_vehicle.license_plate
    
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

# 4. DELETE Route: Remove a vehicle from the fleet registry
@router.delete("/{vehicle_id}")
def delete_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    db_vehicle = db.query(DBVehicle).filter(DBVehicle.id == vehicle_id).first()
    if not db_vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
        
    db.delete(db_vehicle)
    db.commit()
    return {"message": f"Vehicle with ID {vehicle_id} successfully deleted"}

