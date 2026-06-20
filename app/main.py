from fastapi import FastAPI
from app.database import engine, Base
from app.routes import vehicles, drivers, trips

Base.metadata.create_all(bind=engine)

# Set up metadata details for the automated interactive docs layout
app = FastAPI(
    title="LERO Fleet Management API",
    description="Secured, production-grade REST API built with FastAPI for commercial fleet operations.",
    version="1.0.0"
)

# Mount all modular domain routers under the absolute enterprise v1 api path
app.include_router(vehicles.router, prefix="/api/v1")
app.include_router(drivers.router, prefix="/api/v1")
app.include_router(trips.router, prefix="/api/v1")

@app.get("/")
def home():
    return {
        "status": "online",
        "project": "LERO Fleet Management System API",
        "api_version": "v1",
        "documentation": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

