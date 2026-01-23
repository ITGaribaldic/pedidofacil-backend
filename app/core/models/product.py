from app.core.models.base import Base
from sqlalchemy import Column, Integer, String, DateTime,func,Boolean,Float

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    price =Column(Float,nullable=False)
    stock = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())