from fastapi import FastAPI, Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader
from app.database import engine, Base
from app.routes import vehicles, drivers, trips

# Define the expected secret token header name
API_KEY_NAME = "X-API-KEY"
API_KEY = "LERO_SECRET_FLEET_TOKEN_2026"  # In a production app, this would live in a hidden .env file
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# Security dependency to validate requests
def get_api_key(header_value: str = Security(api_key_header)):
    if header_value == API_KEY:
        return header_value
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Unauthorized: Invalid or missing LERO Security API Key"
    )

Base.metadata.create_all(bind=engine)

# Pass the security dependency globally to lock down the entire API dashboard
app = FastAPI(title="LERO Fleet API Secured", dependencies=[Security(get_api_key)])

app.include_router(vehicles.router)
app.include_router(drivers.router)
app.include_router(trips.router)

@app.get("/")
def home():
    return {"message": "LERO Fleet API running securely"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

