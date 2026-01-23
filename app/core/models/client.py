# Define modelo Client com colunas correspondentes à tabela 'clients'
from app.core.models.base import Base
from sqlalchemy import Column, Integer, String, DateTime,func,Boolean

class Client(Base):
    __tablename__ = 'clients'


    id = Column(Integer, primary_key=True, index=True) # ID único do cliente
    name = Column(String(100),nullable=False) # Nome do cliente
    email = Column(String(100), unique=True, nullable=False) # Email único
    phone = Column(String(20), nullable=True) # Telefone opcional
    adress = Column(String(200), nullable=True) # Endereço opcional
    creadet_at = Column(DateTime, server_default=func.now()) # Data de criação
    active = Column(Boolean, default=True) # Status ativo/inativo