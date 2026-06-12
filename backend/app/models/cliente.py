from app.database.base import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func


class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    correo = Column(String(150), unique=True)
    telefono = Column(String(20))

    fecha_creacion = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )