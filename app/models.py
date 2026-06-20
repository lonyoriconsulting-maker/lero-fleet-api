from sqlalchemy import Column, Integer, String
from app.database import Base

class DBVehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    make = Column(String, index=True)
    model = Column(String)
    year = Column(Integer)
    license_plate = Column(String, unique=True, index=True)

# Keep your existing DBVehicle model at the top, just add this to the bottom:
from sqlalchemy import Column, Integer, String

class DBDriver(Base):
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    license_number = Column(String, unique=True, index=True)
    phone_number = Column(String)

# Keep your existing code at the top, append this to the very bottom:
from sqlalchemy import Column, Integer, String, Float, ForeignKey

class DBTrip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)
    driver_id = Column(Integer, ForeignKey("drivers.id"), nullable=False)
    start_location = Column(String)
    end_location = Column(String)
    distance_km = Column(Float)
    fuel_used_liters = Column(Float)

