from app.database.base import Base
from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    Numeric,
    DateTime
)
from sqlalchemy.sql import func


class Venta(Base):
    __tablename__ = "ventas"

    id = Column(Integer, primary_key=True, index=True)

    cliente_id = Column(
        Integer,
        ForeignKey("clientes.id"),
        nullable=False
    )

    fecha_venta = Column(
        DateTime,
        server_default=func.now()
    )

    total = Column(
        Numeric(10, 2),
        default=0
    )