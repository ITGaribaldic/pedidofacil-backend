from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.core.dependencies import get_current_user  # Dependência para autenticação do usuário

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

# Cria um router FastAPI para endpoints relacionados a clientes
router = APIRouter(
    prefix="/clients",
    tags=["clients"]
)

# ---------------------- ENDPOINTS ----------------------

@router.get("/", response_model=List[ClientRead])
def read_clients(
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(100, ge=1, le=200, description="Limite de registros por página"),
    db: Session = Depends(get_db)
):
    """
    Lista clientes ativos com paginação.
    
    - **skip**: número de registros a pular (para paginação)
    - **limit**: número máximo de registros retornados
    """
    clients = get_clients(db, skip=skip, limit=limit)
    return clients


@router.get("/{client_id}", response_model=ClientRead)
def read_client(client_id: int, db: Session = Depends(get_db)):
    """
    Retorna um cliente específico pelo ID.
    
    Retorna 404 se o cliente não for encontrado.
    """
    db_client = get_client(db, client_id)
    if db_client is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado"
        )
    return db_client


@router.post("/", response_model=ClientRead, status_code=status.HTTP_201_CREATED)
def create_new_client(
    client: ClientCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),  # Garante que apenas usuário autenticado pode criar
):
    """
    Cria um novo cliente associado ao usuário autenticado.
    
    - **client**: dados do cliente (nome, email, telefone, endereço)
    - **current_user**: usado para associar o cliente ao usuário que criou
    """
    return create_client(
        db=db,
        client=client,
        user_id=current_user.id,
    )


@router.put("/{client_id}", response_model=ClientRead)
def update_existing_client(
    client_id: int,
    client_update: ClientUpdate,
    db: Session = Depends(get_db)
):
    """
    Atualiza os dados de um cliente existente.
    
    Retorna 404 se o cliente não for encontrado.
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
    
    Retorna 404 se o cliente não existir.
    DELETE 204 não retorna corpo.
    """
    success = delete_client(db, client_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado"
        )


@router.patch("/{client_id}/deactivate", response_model=ClientRead)
def deactivate_existing_client(client_id: int, db: Session = Depends(get_db)):
    """
    Desativa um cliente (soft delete), apenas marcando active=False.
    
    Retorna 404 se o cliente não existir.
    """
    deactivated_client = deactivate_client(db, client_id)
    if deactivated_client is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado"
        )
    return deactivated_client
