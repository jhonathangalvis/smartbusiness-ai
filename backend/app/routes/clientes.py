from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.cliente import Cliente
from app.schemas.cliente import (
    ClienteResponse,
    ClienteCreate,
    ClienteUpdate
)

router = APIRouter()


# Obtener todos los clientes
@router.get(
    "/clientes",
    response_model=list[ClienteResponse]
)
def obtener_clientes(
    db: Session = Depends(get_db)
):
    return db.query(Cliente).all()


# Obtener cliente por ID
@router.get(
    "/clientes/{cliente_id}",
    response_model=ClienteResponse
)
def obtener_cliente(
    cliente_id: int,
    db: Session = Depends(get_db)
):
    cliente = (
        db.query(Cliente)
        .filter(Cliente.id == cliente_id)
        .first()
    )

    if not cliente:
        raise HTTPException(
            status_code=404,
            detail="Cliente no encontrado"
        )

    return cliente


# Crear cliente
@router.post(
    "/clientes",
    response_model=ClienteResponse
)
def crear_cliente(
    cliente: ClienteCreate,
    db: Session = Depends(get_db)
):
    cliente_existente = (
        db.query(Cliente)
        .filter(Cliente.correo == cliente.correo)
        .first()
    )

    if cliente_existente:
        raise HTTPException(
            status_code=409,
            detail="Ya existe un cliente con ese correo"
        )

    nuevo_cliente = Cliente(
        nombre=cliente.nombre,
        correo=cliente.correo,
        telefono=cliente.telefono
    )

    db.add(nuevo_cliente)
    db.commit()
    db.refresh(nuevo_cliente)

    return nuevo_cliente


# Actualizar cliente
@router.put(
    "/clientes/{cliente_id}",
    response_model=ClienteResponse
)
def actualizar_cliente(
    cliente_id: int,
    cliente_data: ClienteUpdate,
    db: Session = Depends(get_db)
):
    cliente = (
        db.query(Cliente)
        .filter(Cliente.id == cliente_id)
        .first()
    )

    if not cliente:
        raise HTTPException(
            status_code=404,
            detail="Cliente no encontrado"
        )

    correo_existente = (
        db.query(Cliente)
        .filter(
            Cliente.correo == cliente_data.correo,
            Cliente.id != cliente_id
        )
        .first()
    )

    if correo_existente:
        raise HTTPException(
            status_code=409,
            detail="Ya existe otro cliente con ese correo"
        )

    cliente.nombre = cliente_data.nombre
    cliente.correo = cliente_data.correo
    cliente.telefono = cliente_data.telefono

    db.commit()
    db.refresh(cliente)

    return cliente


# Eliminar cliente
@router.delete("/clientes/{cliente_id}")
def eliminar_cliente(
    cliente_id: int,
    db: Session = Depends(get_db)
):
    cliente = (
        db.query(Cliente)
        .filter(Cliente.id == cliente_id)
        .first()
    )

    if not cliente:
        raise HTTPException(
            status_code=404,
            detail="Cliente no encontrado"
        )

    db.delete(cliente)
    db.commit()

    return {
        "message": "Cliente eliminado correctamente"
    }