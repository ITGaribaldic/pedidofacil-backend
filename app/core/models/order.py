# Define modelo Order com colunas e relacionamentos da tabela 'orders'
from app.core.models.base import Base
from sqlalchemy import Column, Integer, Float, DateTime, Boolean, ForeignKey, func
from sqlalchemy.orm import relationship

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True) # ID único do pedido
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)  # ID do cliente
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)  # ID do produto
    quantity = Column(Integer, default=1) # Quantidade do produto
    total_price = Column(Float, nullable=False) # Valor total do pedido
    created_at = Column(DateTime, server_default=func.now())  # Data de criação
    completed = Column(Boolean, default=False) # Status do pedido

    client = relationship("Client", backref="orders") # Relacionamento com cliente
    product = relationship("Product", backref="orders") # Relacionamento com produto