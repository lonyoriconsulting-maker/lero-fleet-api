from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import DBDriver
from app.schemas import DriverCreate, DriverResponse
from app.dependencies import get_current_user_role  # Clean import

router = APIRouter(prefix="/drivers", tags=["Drivers"])

# 1. POST Route: Register driver (MANAGER ONLY)
@router.post("", response_model=DriverResponse)
def add_driver(driver: DriverCreate, db: Session = Depends(get_db), role: str = Depends(get_current_user_role)):
    if role != "manager":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied: Managers only")
    
    db_driver = db.query(DBDriver).filter(DBDriver.license_number == driver.license_number).first()
    if db_driver:
        raise HTTPException(status_code=400, detail="License number already registered")
    
    new_driver = DBDriver(first_name=driver.first_name, last_name=driver.last_name, license_number=driver.license_number, phone_number=driver.phone_number)
    db.add(new_driver)
    db.commit()
    db.refresh(new_driver)
    return new_driver

# 2. GET Route: Fetch all drivers (MANAGER ONLY)
@router.get("", response_model=List[DriverResponse])
def get_drivers(db: Session = Depends(get_db), role: str = Depends(get_current_user_role)):
    if role != "manager":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied: Managers only")
    return db.query(DBDriver).all()

