# app/api/routes/products.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.product import ProductCreate, ProductUpdate, ProductRead
from app.services.product_service import (
    get_product,
    get_products,
    create_product,
    update_product,
    delete_product
)
router = APIRouter(
    prefix="/products",
    tags=["products"]
)


@router.get("/", response_model=List[ProductRead])
def read_products(
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(100, ge=1, le=200, description="Limite de registros por página"),
    db: Session = Depends(get_db)
):
    """
    Retorna uma lista de produtos com paginação.
    """
    products = get_products(db, skip=skip, limit=limit)
    return products


@router.get("/{product_id}", response_model=ProductRead)
def read_product(product_id: int, db: Session = Depends(get_db)):
    """
    Retorna um produto específico pelo ID.
    """
    db_product = get_product(db, product_id)
    if db_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado"
        )
    return db_product


@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_new_product(product: ProductCreate, db: Session = Depends(get_db)):
    """
    Cria um novo produto.
    """
    return create_product(db, product)


@router.put("/{product_id}", response_model=ProductRead)
def update_existing_product(
    product_id: int,
    product_update: ProductUpdate,
    db: Session = Depends(get_db)
):
    """
    Atualiza os dados de um produto existente.
    """
    updated_product = update_product(db, product_id, product_update)
    if updated_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado"
        )
    return updated_product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_product(product_id: int, db: Session = Depends(get_db)):
    """
    Remove um produto do sistema.
    """
    success = delete_product(db, product_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado"
        )