from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.models.venta import Venta
from app.models.cliente import Cliente
from app.models.producto import Producto
from app.models.detalle_venta import DetalleVenta

from app.schemas.venta import (
    VentaCreate,
    VentaResponse
)

from app.schemas.detalle_venta import (
    DetalleVentaCreate,
    DetalleVentaResponse
)

router = APIRouter()


# Obtener todas las ventas
@router.get(
    "/ventas",
    response_model=list[VentaResponse]
)
def obtener_ventas(
    db: Session = Depends(get_db)
):
    return db.query(Venta).all()


# Crear venta
@router.post(
    "/ventas",
    response_model=VentaResponse
)
def crear_venta(
    venta: VentaCreate,
    db: Session = Depends(get_db)
):
    cliente = (
        db.query(Cliente)
        .filter(
            Cliente.id == venta.cliente_id
        )
        .first()
    )

    if not cliente:
        raise HTTPException(
            status_code=404,
            detail="Cliente no encontrado"
        )

    nueva_venta = Venta(
        cliente_id=venta.cliente_id,
        total=0
    )

    db.add(nueva_venta)

    db.commit()

    db.refresh(nueva_venta)

    return nueva_venta


# Obtener una venta por ID
@router.get(
    "/ventas/{venta_id}",
    response_model=VentaResponse
)
def obtener_venta(
    venta_id: int,
    db: Session = Depends(get_db)
):
    venta = (
        db.query(Venta)
        .filter(
            Venta.id == venta_id
        )
        .first()
    )

    if not venta:
        raise HTTPException(
            status_code=404,
            detail="Venta no encontrada"
        )

    return venta


# Obtener detalles de una venta
@router.get(
    "/ventas/{venta_id}/detalles",
    response_model=list[DetalleVentaResponse]
)
def obtener_detalles_venta(
    venta_id: int,
    db: Session = Depends(get_db)
):
    venta = (
        db.query(Venta)
        .filter(
            Venta.id == venta_id
        )
        .first()
    )

    if not venta:
        raise HTTPException(
            status_code=404,
            detail="Venta no encontrada"
        )

    detalles = (
        db.query(DetalleVenta)
        .filter(
            DetalleVenta.venta_id == venta_id
        )
        .all()
    )

    return detalles


# Agregar producto a una venta
@router.post(
    "/ventas/{venta_id}/detalle",
    response_model=DetalleVentaResponse
)
def agregar_producto_a_venta(
    venta_id: int,
    detalle: DetalleVentaCreate,
    db: Session = Depends(get_db)
):
    venta = (
        db.query(Venta)
        .filter(
            Venta.id == venta_id
        )
        .first()
    )

    if not venta:
        raise HTTPException(
            status_code=404,
            detail="Venta no encontrada"
        )

    producto = (
        db.query(Producto)
        .filter(
            Producto.id == detalle.producto_id
        )
        .first()
    )

    if not producto:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    if producto.stock < detalle.cantidad:
        raise HTTPException(
            status_code=400,
            detail="Stock insuficiente"
        )

    producto.stock -= detalle.cantidad

    subtotal = (
        float(producto.precio)
        * detalle.cantidad
    )

    nuevo_detalle = DetalleVenta(
        venta_id=venta_id,
        producto_id=detalle.producto_id,
        cantidad=detalle.cantidad,
        precio_unitario=producto.precio,
        subtotal=subtotal
    )

    db.add(nuevo_detalle)

    venta.total = (
        float(venta.total)
        + subtotal
    )

    db.commit()

    db.refresh(nuevo_detalle)

    return nuevo_detalle