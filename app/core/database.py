from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings


# URL de conexão com o banco PostgreSQL
DATABASE_URL = "postgresql+psycopg2://postgres:261223@localhost:5432/pedidofacil"

# Cria engine SQLAlchemy com logging baseado no debug
engine = create_engine(
    DATABASE_URL,
    echo=settings.debug
)
# Cria fábrica de sessões para interação com o banco
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
# Base para declaração de modelos ORM
Base = declarative_base()

