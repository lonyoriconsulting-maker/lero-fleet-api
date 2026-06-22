from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# Initialize app and templates
app = FastAPI(title="LERO Fleet Management API")
templates = Jinja2Templates(directory="app/templates")

# Error-proof dashboard route (No model dependencies)
@app.get("/dashboard", response_class=HTMLResponse)
def read_dashboard(request: Request):
    # Dummy data list to cleanly render your new HTML log table rows
    mock_trips = [
        {"id": 1, "driver_id": 101, "vehicle_id": 201, "route_name": "Arusha-Moshi Express", "distance": 85.0, "fuel_used": 12.5},
        {"id": 2, "driver_id": 102, "vehicle_id": 202, "route_name": "Njiro Local Grid", "distance": 14.2, "fuel_used": 3.1}
    ]
    
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "total_drivers": 12,
            "total_vehicles": 8,
            "total_trips": 2,
            "total_distance": 99.2,
            "total_fuel": 15.6,
            "recent_trips": mock_trips
        }
    )

