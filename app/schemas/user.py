from pydantic import BaseModel, EmailStr, constr
from typing import Optional, Annotated
from datetime import datetime

class UserCreate(BaseModel):
    """ Valida dados de entrada para criar novo usuário"""
    username: Optional[Annotated[str, constr(max_length=50)]]
    email: Annotated[EmailStr, ...]
    full_name: Optional[Annotated[str, constr(max_length=100)]]
    password: Annotated[str, constr(min_length=8)]

class UserRead(BaseModel):
    """Define os dados e usuário retornados pela API (não inclui senha)"""
    id: int
    username: Optional[str]
    email: EmailStr
    full_name: Optional[str]
    created_at: datetime

    model_config = {
        "from_attributes": True
    }

class UserLogin(BaseModel):
    """Valida dados de entrada para login"""
    email: EmailStr
    password : str