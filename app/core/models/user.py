# Define modelo User com colunas da tabela 'users'
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime, func
from app.core.models.base import Base
from passlib.context import CryptContext
from typing import Optional

# Configuração do hash de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    """
    Modelo User representando a tabela 'users'.

    Responsável por armazenar informações de usuários, incluindo
    dados pessoais, email único e hash de senha. Inclui métodos
    para gerenciar a senha com segurança.
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[Optional[str]] = mapped_column(String(50), unique=True, nullable=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    full_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    password_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


# Define a senha do usuário, armazenando apenas o hash
    def set_password(self, password: str):
        self.password_hash = pwd_context.hash(password)

    # Verifica se a senha fornecida bate com o hash
    def check_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.password_hash)