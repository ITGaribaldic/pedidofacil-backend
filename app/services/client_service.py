from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from app.core.models.client import Client
from app.schemas.client import ClientCreate, ClientUpdate
from typing import List, Optional

def get_client(db: Session, client_id: int) -> Optional[Client]:
    """
    Retorna um cliente pelo ID.
    Retorna None se não existir.
    """
    return db.query(Client).filter(Client.id == client_id).first()


def get_clients(db: Session, skip: int = 0, limit: int = 100) -> List[Client]:
    """
    Retorna todos os clientes ativos com paginação.
    """
    return (
        db.query(Client)
        .filter(Client.active == True)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_client(db: Session, client: ClientCreate, user_id: int) -> Client:
    """
    Cria um novo cliente.
    Verifica se o email já está cadastrado.
    Atribui o user_id do usuário responsável pelo cadastro.
    """
    existing_client = db.query(Client).filter(Client.email == client.email).first()
    if existing_client:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado para outro cliente"
        )
    
    try:
        db_client = Client(
            name=client.name,
            email=client.email,
            phone=client.phone,
            address=client.address,
            user_id=user_id,
        )

        db.add(db_client)
        db.commit()
        db.refresh(db_client)
        return db_client
    
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar cliente: {str(e)}"
        )


def update_client(db: Session, client_id: int, client_update: ClientUpdate) -> Optional[Client]:
    """
    Atualiza os dados de um cliente existente.
    Verifica se o novo email já está cadastrado para outro cliente.
    Retorna o cliente atualizado ou None se não existir.
    """
    db_client = get_client(db, client_id)
    if not db_client:
        return None
    
    try:
        update_data = client_update.model_dump(exclude_unset=True)

        # Valida email único
        if "email" in update_data and update_data["email"] != db_client.email:
            existing = db.query(Client).filter(
                Client.email == update_data["email"],
                Client.id != client_id
            ).first()
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email já cadastrado para outro cliente"
                )
        
        # Atualiza os campos fornecidos
        for field, value in update_data.items():
            setattr(db_client, field, value)
        
        db.commit()
        db.refresh(db_client)
        return db_client
    
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar cliente: {str(e)}"
        )


def delete_client(db: Session, client_id: int) -> bool:
    """
    Remove um cliente do banco (deleção física).
    Retorna True se deletado, False se não encontrado.
    """
    db_client = get_client(db, client_id)
    if not db_client:
        return False
    
    try:
        db.delete(db_client)
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao deletar cliente: {str(e)}"
        )
    

def deactivate_client(db: Session, client_id: int) -> Optional[Client]:
    """
    Desativa um cliente (soft delete).
    Apenas marca como active=False sem remover do banco.
    Retorna o cliente desativado ou None se não encontrado.
    """
    db_client = get_client(db, client_id)
    if not db_client:
        return None
    
    try:
        db_client.active = False
        db.commit()
        db.refresh(db_client)
        return db_client
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao desativar cliente: {str(e)}"
        )
