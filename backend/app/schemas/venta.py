from pydantic import BaseModel
from datetime import datetime


class VentaCreate(BaseModel):
    cliente_id: int


class VentaResponse(BaseModel):
    id: int
    cliente_id: int
    total: float
    fecha_venta: datetime

    class Config:
        from_attributes = True