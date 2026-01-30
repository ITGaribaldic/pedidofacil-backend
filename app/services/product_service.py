from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException,status
from app.core.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate
from typing import List, Optional

def get_product(db: Session, product_id: int) -> Optional[Product]:
    """
    Busca um produto pelo ID. Retorna None se não encontrar.
    """
    return db.query(Product).filter(Product.id==product_id).first()

def get_products(db: Session, skip: int = 0, limit:int =100) -> List[Product]:
    """
    Lista produto com paginação.
    """
    return (
        db.query(Product)
        .offset(skip)
        .limit(limit)
        .all()
    )

def create_product(db:Session, product: ProductCreate) -> Product:
    """
    Cria novo produto no banco
    """
    #Verifica se produto com o mesmo já existe()
    existing_product = db.query(Product).filter(Product.name == product.name).first()
    if existing_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Já existe um produto com este nome"
        )
    
    try:
        db_product = Product(
            name=product.name,
            description=product.description,
            price=product.price,
            stock=product.stock
        
        )
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar produto: {str(e)}"
        )

def update_product(db: Session, product_id: int, product_update: ProductUpdate) -> Optional[Product]:
    """
    Atualiza dados de um produto existente
    Retorna o produto atualizado ou None se não encontrado.
    """
    db_product = get_product(db, product_id)
    if not db_product:
        return None
    
    try:
        update_data = product_update.model_dump(exclude_unset=True)

        #Verifica se o novo nome (se fornecido) já pertencea outro produto
        if "name" in update_data and update_data["name"] != db_product.name:
            existing = db.query(Product).filter(
                Product.name == update_data["name"],
                Product.id != product_id
            ).first()
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Já existe outro produto com este nome"
                )
        for field, value in update_data.items():
            setattr(db_product, field, value)
        
        db.commit()
        db.refresh(db_product)
        return db_product
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar produto: {str(e)}"
        )

def delete_product(db: Session, product_id: int) -> bool:
    """
    Remove um produto do banco (deleção física).
    Retorna True se deletado, False se não encontrado.
    """
    db_product = get_product(db, product_id)
    if not db_product:
        return False
    
    try:
        db.delete(db_product)
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao deletar produto: {str(e)}"
        )