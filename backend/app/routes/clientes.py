from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.cliente import Cliente
from app.schemas.cliente import (
    ClienteResponse,
    ClienteCreate
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
    clientes = db.query(Cliente).all()
    return clientes


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