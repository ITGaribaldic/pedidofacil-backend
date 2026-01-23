# Define modelo Product com colunas da tabela 'products'
from app.core.models.base import Base
from sqlalchemy import Column, Integer, String, DateTime,func,Boolean,Float

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True) # ID único do produto
    name = Column(String(100), nullable=False) # Nome do produto
    description = Column(String(255), nullable=True) # Descrição opcional
    price =Column(Float,nullable=False) # Preço do produto
    stock = Column(Integer, default=0) # Quantidade em estoque
    created_at = Column(DateTime, server_default=func.now()) # Data de criação