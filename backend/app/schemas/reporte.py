from pydantic import BaseModel


class ReporteVentaResponse(BaseModel):
    venta_id: int
    cliente: str
    total: float

    class Config:
        from_attributes = True