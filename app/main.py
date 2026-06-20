from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import engine, Base, get_db
from app.models import DBVehicle
from app.schemas import VehicleCreate, VehicleResponse

# Create the database tables automatically if they do not exist
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def home():
    return {"message": "LERO Fleet API running with SQLite"}

# 1. POST Route: Add a vehicle directly to the database
@app.post("/vehicles", response_model=VehicleResponse)
def add_vehicle(vehicle: VehicleCreate, db: Session = Depends(get_db)):
    # Check if a vehicle with the same license plate already exists
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

# 2. GET Route: Fetch all vehicles from the database
@app.get("/vehicles", response_model=List[VehicleResponse])
def get_vehicles(db: Session = Depends(get_db)):
    vehicles = db.query(DBVehicle).all()
    return vehicles

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

