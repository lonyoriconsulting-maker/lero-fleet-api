from pydantic import BaseModel

# Fields required to create a vehicle
class VehicleCreate(BaseModel):
    make: str
    model: str
    year: int
    license_plate: str

# Fields returned when reading a vehicle (includes database ID)
class VehicleResponse(VehicleCreate):
    id: int

    class Config:
        from_attributes = True

