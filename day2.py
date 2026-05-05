

from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="NB-IoT Sensor API",
    description="Learning FastAPI using NB-IoT sensor data",
    version="1.0.0"
)


# Temporary in-memory storage
# Later we will replace this with real database

latest_packt = {}

class NbiotPacket(BaseModel):
    payload: str 
    ip: str | None = None
    port:int | None = None


@app.get("/")
def home():
    return {
        "message": "NB-IoT FastAPI server is running",
        "status": "ok"
    }

@app.get("/health")
def health_check():
    return {
        "service": "Nbiot-api",
        "status": "health"
    }

@app.post("/nbiot")
def receive_nbiot_packet(packet: NbiotPacket):
    global latest_packet

    latest_packet = {
        "payload": packet.payload,
        "ip": packet.ip,
        "port":packet.port,
        "receive_at":datetime.utcnow().isoformat()
    }

    return {
        "status": "received",
        "command": "CALL_FN",
        "data":latest_packet
    }

@app.get("/latest")
def get_latest_packet():
    if not latest_packet:
        return {
            "message": "No NB-IoT packet received"
        }

    return latest_packet

