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

# Keep your existing Vehicle schemas at the top, just add this to the bottom:
from pydantic import BaseModel

class DriverCreate(BaseModel):
    first_name: str
    last_name: str
    license_number: str
    phone_number: str

class DriverResponse(DriverCreate):
    id: int

    class Config:
        from_attributes = True

