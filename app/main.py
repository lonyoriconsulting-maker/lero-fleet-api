from fastapi import FastAPI
from app.database import engine, Base
from app.routes import vehicles, drivers, trips

Base.metadata.create_all(bind=engine)

app = FastAPI(title="LERO Role-Based Fleet API")

app.include_router(vehicles.router)
app.include_router(drivers.router)
app.include_router(trips.router)

@app.get("/")
def home():
    return {"message": "LERO Fleet API running securely with Role-Based access control"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

