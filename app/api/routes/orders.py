from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi import status
from app.core.database import get_db
from app.api.deps import get_current_user
from app.schemas.order import OrderCreate, OrderUpdate, Order, OrderWithItems
from app.services.order_service import OrderService
from app.services.exceptions import NotFoundException, BusinessRuleException
from app.core.models import User

router = APIRouter(
    prefix="/orders",
    tags=["orders"]
)


@router.get("/", response_model=List[Order])
def read_orders(
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(100, ge=1, le=200, description="Limite de registros por página"),
    client_id: Optional[int] = Query(None, description="Filtrar por ID do cliente"),
    status_filter: Optional[str] = Query(None, description="Filtrar por status do pedido"),
    start_date: Optional[datetime] = Query(None, description="Data inicial"),
    end_date: Optional[datetime] = Query(None, description="Data final"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retorna uma lista de pedidos com filtros e paginação.
    """
    try:
        orders, total = OrderService.get_orders(
            db=db,
            current_user_id=current_user.id,
            client_id=client_id,
            status=status_filter,
            start_date=start_date,
            end_date=end_date,
            skip=skip,
            limit=limit
        )
        return orders
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar pedidos: {str(e)}"
        )


@router.get("/{order_id}", response_model=OrderWithItems)
def read_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retorna um pedido específico pelo ID com seus itens.
    """
    try:
        order = OrderService.get_order_by_id(db, order_id, current_user.id)
        return order
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar pedido: {str(e)}"
        )


@router.post("/", response_model=Order, status_code=status.HTTP_201_CREATED)
def create_new_order(
    order: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Cria um novo pedido.
    """
    try:
        new_order = OrderService.create_order(db, order, current_user.id)
        return new_order
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except BusinessRuleException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar pedido: {str(e)}"
        )


@router.patch("/{order_id}/status", response_model=Order)
def update_order_status(
    order_id: int,
    order_update: OrderUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Atualiza o status de um pedido existente.
    """
    try:
        updated_order = OrderService.update_order_status(
            db, order_id, order_update, current_user.id
        )
        return updated_order
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except BusinessRuleException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar status: {str(e)}"
        )


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Remove um pedido do sistema (apenas se estiver pendente).
    """
    try:
        success = OrderService.delete_order(db, order_id, current_user.id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pedido não encontrado"
            )
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except BusinessRuleException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao excluir pedido: {str(e)}"
        )