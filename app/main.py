from fastapi import FastAPI
from app.database import engine, Base
from app.routes import vehicles

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="LERO Fleet API")

# Connect our modular routes
app.include_router(vehicles.router)

@app.get("/")
def home():
    return {"message": "LERO Fleet API running with clean routing"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

