from pydantic import BaseModel


class TopProductoResponse(BaseModel):
    producto: str
    cantidad_vendida: int