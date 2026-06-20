from sqlalchemy import Column, Integer, String
from app.database import Base

class DBVehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    make = Column(String, index=True)
    model = Column(String)
    year = Column(Integer)
    license_plate = Column(String, unique=True, index=True)

