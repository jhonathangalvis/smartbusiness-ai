from pydantic import BaseModel


class DetalleVentaCreate(BaseModel):
    producto_id: int
    cantidad: int


class DetalleVentaResponse(BaseModel):
    id: int
    venta_id: int
    producto_id: int
    cantidad: int
    precio_unitario: float
    subtotal: float

    class Config:
        from_attributes = True