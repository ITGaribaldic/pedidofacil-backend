from app.core.models.base import Base
from sqlalchemy import Column, Integer, String, DateTime,func,Boolean

class Client(Base):
    __tablename__ = 'clients'


    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100),nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20), nullable=True)
    adress = Column(String(200), nullable=True)
    creadet_at = Column(DateTime, server_default=func.now())
    active = Column(Boolean, default=True)