from app.core.models.base import Base
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, func, String
from sqlalchemy.orm import relationship
import enum

# Enum para representar os status possíveis de um pedido
class OrderStatus(enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed" 
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    status = Column(String(20), nullable=False, default=OrderStatus.PENDING.value)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    total = Column(Float, nullable=False, default=0.0)
    created_at = Column(DateTime, server_default=func.now())

    client = relationship("Client", backref="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

    def calculate_total(self):
        """Calcula o total do pedido somando o subtotal de cada item"""
        if self.items:
            self.total = sum(item.subtotal for item in self.items)
        else:
            self.total = 0.0
        return self.total
