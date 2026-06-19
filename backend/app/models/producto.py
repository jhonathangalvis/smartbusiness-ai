from app.database.base import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Numeric,
    DateTime
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)

    nombre = Column(String(100), nullable=False)

    descripcion = Column(Text)

    precio = Column(Numeric(10, 2), nullable=False)

    stock = Column(Integer, default=0)

    fecha_creacion = Column(
        DateTime,
        server_default=func.now()
    )

    detalles = relationship(
        "DetalleVenta",
        back_populates="producto"
    )