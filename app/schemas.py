from pydantic import BaseModel, Field, field_validator
from datetime import datetime

# Current year constraint for validation
CURRENT_YEAR = 2026

# --- VEHICLE SCHEMAS ---
class VehicleCreate(BaseModel):
    make: str = Field(..., min_length=1, max_length=50)
    model: str = Field(..., min_length=1, max_length=50)
    year: int = Field(..., description="The vehicle production year")
    license_plate: str = Field(..., min_length=3, max_length=15)

    @field_validator("year")
    @classmethod
    def validate_year(cls, value: int) -> int:
        if value < 1900 or value > CURRENT_YEAR:
            raise ValueError(f"Year must be between 1900 and {CURRENT_YEAR}")
        return value

    @field_validator("license_plate")
    @classmethod
    def clean_plate(cls, value: str) -> str:
        # Strip spacing and convert to clean uppercase standard
        return value.strip().upper()

class VehicleResponse(VehicleCreate):
    id: int

    class Config:
        from_attributes = True


# --- DRIVER SCHEMAS ---
class DriverCreate(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    license_number: str = Field(..., min_length=5, max_length=20)
    phone_number: str = Field(..., min_length=7, max_length=20)

    @field_validator("license_number")
    @classmethod
    def clean_license(cls, value: str) -> str:
        return value.strip().upper()


class DriverResponse(DriverCreate):
    id: int

    class Config:
        from_attributes = True


# --- TRIP SCHEMAS ---
class TripCreate(BaseModel):
    vehicle_id: int = Field(..., gt=0)
    driver_id: int = Field(..., gt=0)
    start_location: str = Field(..., min_length=2)
    end_location: str = Field(..., min_length=2)
    distance_km: float = Field(..., gt=0.0, description="Distance must be greater than zero")
    fuel_used_liters: float = Field(..., gt=0.0, description="Fuel used must be greater than zero")

class TripResponse(TripCreate):
    id: int

    class Config:
        from_attributes = True

