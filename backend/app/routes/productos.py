from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.producto import Producto
from app.schemas.producto import (
    ProductoCreate,
    ProductoUpdate,
    ProductoResponse
)

router = APIRouter()


# Obtener todos los productos
@router.get(
    "/productos",
    response_model=list[ProductoResponse]
)
def obtener_productos(
    db: Session = Depends(get_db)
):
    return db.query(Producto).all()


# Obtener producto por ID
@router.get(
    "/productos/{producto_id}",
    response_model=ProductoResponse
)
def obtener_producto(
    producto_id: int,
    db: Session = Depends(get_db)
):
    producto = (
        db.query(Producto)
        .filter(Producto.id == producto_id)
        .first()
    )

    if not producto:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    return producto


# Crear producto
@router.post(
    "/productos",
    response_model=ProductoResponse
)
def crear_producto(
    producto: ProductoCreate,
    db: Session = Depends(get_db)
):
    nuevo_producto = Producto(
        nombre=producto.nombre,
        descripcion=producto.descripcion,
        precio=producto.precio,
        stock=producto.stock
    )

    db.add(nuevo_producto)

    db.commit()

    db.refresh(nuevo_producto)

    return nuevo_producto


# Actualizar producto
@router.put(
    "/productos/{producto_id}",
    response_model=ProductoResponse
)
def actualizar_producto(
    producto_id: int,
    producto_data: ProductoUpdate,
    db: Session = Depends(get_db)
):
    producto = (
        db.query(Producto)
        .filter(Producto.id == producto_id)
        .first()
    )

    if not producto:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    producto.nombre = producto_data.nombre
    producto.descripcion = producto_data.descripcion
    producto.precio = producto_data.precio
    producto.stock = producto_data.stock

    db.commit()

    db.refresh(producto)

    return producto


# Eliminar producto
@router.delete("/productos/{producto_id}")
def eliminar_producto(
    producto_id: int,
    db: Session = Depends(get_db)
):
    producto = (
        db.query(Producto)
        .filter(Producto.id == producto_id)
        .first()
    )

    if not producto:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    db.delete(producto)

    db.commit()

    return {
        "message": "Producto eliminado correctamente"
    }