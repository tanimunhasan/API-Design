# store multiple received packets

from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="NB-IoT Sensor API",
    description="Learning FastAPI using NB-IoT sensor data",
    version="1.0.0"
)

# Temporary in-memory storage
# This will reset when the server restarts.

packet_history = []

class NbiotPacket(BaseModel):
    payload: str
    ip: str | None = None
    port: int | None = None


@app.get("/")
def home():
    return {
        "message": "NB-IoT FastAPI server is running",
        "status":"ok"
    }

@app.get("/health")
def health_check():
    return {
        "service": "nbiot_api",
        "status": "healthy"
    }

@app.post("/nbiot")
def receive_nbiot_packet(packet: NbiotPacket):
    packet_record = {
        "id": len(packet_history) + 1,
        "payload": packet.payload,
        "ip": packet.ip,
        "port": packet.port,
        "receive_at": datetime.utcnow().isoformat()
    }

    packet_history.append(packet_record)

    return {
        "status": "received",
        "command": "CALL_FN",
        "data": packet_record
    }

@app.get("/latest")
def get_latest_packet():
    if not packet_history:
        return {
            "message": "No NB-IoT packet received yet"
        }

    return packet_history[-1]    

@app.get("/history")
def get_packet_history():
    return {
        "total": len(packet_history),
        "data": packet_history
    }

@app.get("/count")
def get_packet_count():
    return {
        "total_packets": len(packet_history)
    }

@app.delete("/history")
def clear_packet_history():
    packet_history.clear()

    return {
        "status": "cleared",
        "message": "All packet history has been removed"
    }

