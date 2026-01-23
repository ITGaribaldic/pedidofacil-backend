# Define modelo User com colunas da tabela 'users'
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime, func
from app.core.models.base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True) # ID único do usuário
    username: Mapped[str | None] = mapped_column(String(50), unique=True, nullable=True) # Nome de usuário opcional
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False) # Email único obrigatório
    full_name: Mapped[str | None] = mapped_column(String(100), nullable=True) # Nome completo opcional
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now()) # Data de criação