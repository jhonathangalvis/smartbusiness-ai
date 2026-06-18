from pydantic import BaseModel


class KPIResponse(BaseModel):
    total_clientes: int
    total_productos: int
    total_ventas: int
    ingresos_totales: float