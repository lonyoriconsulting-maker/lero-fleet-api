from fastapi import FastAPI, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import SessionLocal, engine
from app.models import Base, DBTrip
# Import your router files
from app.routes import drivers, vehicles, trips

# Initialize Database Architecture
Base.metadata.create_all(bind=engine)

app = FastAPI(title="LERO Fleet Management API")

# Initialize Jinja2 Templates directory mounting
templates = Jinja2Templates(directory="app/templates")

# DB Dependency injection wrapper
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Enterprise Path Prefix Routing Groupings
app.include_router(drivers.router, prefix="/api/v1")
app.include_router(vehicles.router, prefix="/api/v1")
app.include_router(trips.router, prefix="/api/v1")

# ROOT WEB ROUTE: Serves styled HTML home screen dashboard UI
@app.get("/", response_class=HTMLResponse)
def read_dashboard(request: Request, db: Session = Depends(get_db)):
    # Pull items from your fleet database configuration
    trips_data = db.query(DBTrip).order_by(DBTrip.id.desc()).all()
    
    # Run rapid arithmetic aggregates on metrics
    total_distance = sum(t.distance_km for t in trips_data) if trips_data else 0.0
    total_fuel = sum(t.fuel_used_liters for t in trips_data) if trips_data else 0.0

    return templates.TemplateResponse("dashboard.html", {
        "request": request, 
        "trips": trips_data,
        "total_distance": total_distance,
        "total_fuel": total_fuel
    })
