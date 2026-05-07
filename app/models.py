from pydantic import BaseModel


class NbiotPacket(BaseModel):
    payload: str
    ip: str | None = None
    port: int | None = None