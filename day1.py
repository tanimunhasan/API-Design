from fastapi import FastAPI

app = FastAPI(
    title= "NB-IoT Sensor API",
    description= "Learning FastAPI using NB-IoT sensor data",
    version="1.0.0"
)

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
        "status": "healthy"
    }
