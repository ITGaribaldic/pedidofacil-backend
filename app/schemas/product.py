from pydantic import BaseModel, constr
from typing import Optional, Annotated
from datetime import datetime

class ProductBase(BaseModel):
    """Base comum para produto"""
    name: Annotated[str, constr(max_length=100)]
    description: Optional[Annotated[str,constr(max_length=255)]] = None
    price : float
    stock: int=0

class ProductCreate(ProductBase):
    """Valida dados de entrada para criar novo produto"""
    pass

class ProductUpdate(BaseModel):
    """Valida dados de entrada para atualizar produto (todos opcionais)"""
    name: Optional[Annotated[str, constr(max_length=100)]] = None
    descriptional : Optional[Annotated[str,constr(max_length=255)]] = None
    price: Optional[float] = None
    stock: Optional[int] = None

class ProductRead(ProductBase):
    """Define os dados de produto retornados pela API"""
    id: int
    created_at: datetime
    model_config = {
        "from_attributes": True
    }