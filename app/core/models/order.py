from app.core.models.base import Base
from sqlalchemy import Column, Integer, Float, DateTime, Boolean, ForeignKey, func
from sqlalchemy.orm import relationship

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)  # corrigido
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)  # corrigido
    quantity = Column(Integer, default=1)
    total_price = Column(Float, nullable=False)
    created_at = Column(DateTime, server_default=func.now())  # corrigido
    completed = Column(Boolean, default=False)

    client = relationship("Client", backref="orders")
    product = relationship("Product", backref="orders")