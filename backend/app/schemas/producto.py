from pydantic import BaseModel
from datetime import datetime


class ProductoCreate(BaseModel):
    nombre: str
    descripcion: str
    precio: float
    stock: int


class ProductoUpdate(BaseModel):
    nombre: str
    descripcion: str
    precio: float
    stock: int


class ProductoResponse(BaseModel):
    id: int
    nombre: str
    descripcion: str
    precio: float
    stock: int
    fecha_creacion: datetime

    class Config:
        from_attributes = True