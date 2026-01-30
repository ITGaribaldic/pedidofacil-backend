from pydantic import BaseModel, EmailStr, constr
from typing import Optional, Annotated
from datetime import datetime


class ClientBase(BaseModel):
    """Base comum para cliente"""
    name: Annotated[str, constr(max_length=100)]
    email: Annotated[EmailStr, ...]
    phone: Optional[Annotated[str, constr(max_length=20)]] = None
    address: Optional[Annotated[str, constr(max_length=200)]] = None


class ClientCreate(ClientBase):
    """Valida dados de entrada para criar novo cliente"""
    pass


class ClientUpdate(BaseModel):
    """Valida dados de entrada para atualizar cliente (todos opcionais)"""
    name: Optional[Annotated[str, constr(max_length=100)]] = None
    email: Optional[Annotated[EmailStr, ...]] = None
    phone: Optional[Annotated[str, constr(max_length=20)]] = None
    address: Optional[Annotated[str, constr(max_length=200)]] = None
    active: Optional[bool] = None


class ClientRead(ClientBase):
    """Define os dados de cliente retornados pela API"""
    id: int
    active: bool
    created_at: datetime

    model_config = {
        "from_attributes": True
    }