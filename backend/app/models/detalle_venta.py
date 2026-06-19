from app.database.base import Base
from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    Numeric
)
from sqlalchemy.orm import relationship


class DetalleVenta(Base):
    __tablename__ = "detalle_venta"

    id = Column(Integer, primary_key=True, index=True)

    venta_id = Column(
        Integer,
        ForeignKey("ventas.id"),
        nullable=False
    )

    producto_id = Column(
        Integer,
        ForeignKey("productos.id"),
        nullable=False
    )

    cantidad = Column(Integer, nullable=False)

    precio_unitario = Column(
        Numeric(10, 2),
        nullable=False
    )

    subtotal = Column(
        Numeric(10, 2),
        nullable=False
    )

    venta = relationship(
        "Venta",
        back_populates="detalles"
    )

    producto = relationship(
        "Producto",
        back_populates="detalles"
    )