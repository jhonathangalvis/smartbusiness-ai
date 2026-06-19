from pydantic import BaseModel


class TopClienteResponse(BaseModel):
    cliente: str
    total_compras: float