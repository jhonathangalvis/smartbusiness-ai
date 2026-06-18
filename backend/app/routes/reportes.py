from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.models.venta import Venta
from app.models.cliente import Cliente
from app.models.detalle_venta import DetalleVenta
from app.models.producto import Producto

from sqlalchemy import func

from app.models.producto import Producto

router = APIRouter()


# Reporte general de ventas
@router.get("/reporte/ventas")
def reporte_ventas(
    db: Session = Depends(get_db)
):
    ventas = (
        db.query(
            Venta.id.label("venta_id"),
            Cliente.nombre.label("cliente"),
            Venta.total
        )
        .join(
            Cliente,
            Cliente.id == Venta.cliente_id
        )
        .all()
    )

    resultado = []

    for venta in ventas:
        resultado.append({
            "venta_id": venta.venta_id,
            "cliente": venta.cliente,
            "total": float(venta.total)
        })

    return resultado


# Reporte detallado de ventas
@router.get("/reporte/detalle-ventas")
def reporte_detalle_ventas(
    db: Session = Depends(get_db)
):
    datos = (
        db.query(
            Venta.id.label("venta_id"),
            Cliente.nombre.label("cliente"),
            Producto.nombre.label("producto"),
            DetalleVenta.cantidad,
            DetalleVenta.subtotal
        )
        .join(
            Cliente,
            Cliente.id == Venta.cliente_id
        )
        .join(
            DetalleVenta,
            DetalleVenta.venta_id == Venta.id
        )
        .join(
            Producto,
            Producto.id == DetalleVenta.producto_id
        )
        .all()
    )

    resultado = []

    for fila in datos:
        resultado.append({
            "venta_id": fila.venta_id,
            "cliente": fila.cliente,
            "producto": fila.producto,
            "cantidad": fila.cantidad,
            "subtotal": float(fila.subtotal)
        })

    return resultado

@router.get("/reporte/kpis")
def obtener_kpis(
    db: Session = Depends(get_db)
):
    total_clientes = db.query(Cliente).count()

    total_productos = db.query(Producto).count()

    total_ventas = db.query(Venta).count()

    ingresos_totales = (
        db.query(
            func.sum(Venta.total)
        )
        .scalar()
        or 0
    )

    return {
        "total_clientes": total_clientes,
        "total_productos": total_productos,
        "total_ventas": total_ventas,
        "ingresos_totales": float(ingresos_totales)
    }