from pydantic import BaseModel, EmailStr
from datetime import datetime


class ClienteCreate(BaseModel):
    nombre: str
    correo: EmailStr
    telefono: str


class ClienteUpdate(BaseModel):
    nombre: str
    correo: EmailStr
    telefono: str


class ClienteResponse(BaseModel):
    id: int
    nombre: str
    correo: str
    telefono: str
    fecha_creacion: datetime

    class Config:
        from_attributes = True