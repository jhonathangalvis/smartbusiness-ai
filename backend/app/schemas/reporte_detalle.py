from pydantic import BaseModel


class ReporteDetalleVentaResponse(BaseModel):
    venta_id: int
    cliente: str
    producto: str
    cantidad: int
    subtotal: float