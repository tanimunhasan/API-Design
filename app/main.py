from fastapi import FastAPI

from app.database import DB_PATH, init_database
from app.routes import packets


app = FastAPI(
    title="NB-IoT Sensor API",
    description="Learning FastAPI using NB-IoT sensor data with SQLite database",
    version="1.0.0"
)


init_database()


app.include_router(packets.router)


@app.get("/")
def home():
    return {
        "message": "NB-IoT FastAPI server is running",
        "status": "ok"
    }


@app.get("/health")
def health_check():
    return {
        "service": "nbiot-api",
        "status": "healthy",
        "database": str(DB_PATH)
    }