from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.client import ClientCreate, ClientUpdate, ClientRead
from app.services.client_service import (
    get_client,
    get_clients,
    create_client,
    update_client,
    delete_client,
    deactivate_client
)

router = APIRouter(
    prefix="/clients",
    tags=["clients"]
)


@router.get("/", response_model=List[ClientRead])
def read_clients(
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(100, ge=1, le=200, description="Limite de registros por página"),
    db: Session = Depends(get_db)
):
    """
    Retorna uma lista de clientes com paginação.
    """
    clients = get_clients(db, skip=skip, limit=limit)
    return clients


@router.get("/{client_id}", response_model=ClientRead)
def read_client(client_id: int, db: Session = Depends(get_db)):
    """
    Retorna um cliente específico pelo ID.
    """
    db_client = get_client(db, client_id)
    if db_client is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado"
        )
    return db_client


@router.post("/", response_model=ClientRead, status_code=status.HTTP_201_CREATED)
def create_new_client(client: ClientCreate, db: Session = Depends(get_db)):
    """
    Cria um novo cliente.
    """
    return create_client(db, client)


@router.put("/{client_id}", response_model=ClientRead)
def update_existing_client(
    client_id: int,
    client_update: ClientUpdate,
    db: Session = Depends(get_db)
):
    """
    Atualiza os dados de um cliente existente.
    """
    updated_client = update_client(db, client_id, client_update)
    if updated_client is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado"
        )
    return updated_client


@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_client(client_id: int, db: Session = Depends(get_db)):
    """
    Remove um cliente do sistema (deleção física).
    """
    success = delete_client(db, client_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado"
        )
    # Não retorna conteúdo em DELETE 204


@router.patch("/{client_id}/deactivate", response_model=ClientRead)
def deactivate_existing_client(client_id: int, db: Session = Depends(get_db)):
    """
    Desativa um cliente (soft delete).
    """
    deactivated_client = deactivate_client(db, client_id)
    if deactivated_client is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado"
        )
    return deactivated_client