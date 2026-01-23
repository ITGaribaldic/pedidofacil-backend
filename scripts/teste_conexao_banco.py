from app.core.database import SessionLocal
from sqlalchemy import text

# Testa a conexão com o banco de dados
def test_connection():
    db = SessionLocal() # Cria sessão
    try:
        db.execute(text("SELECT 1")) # Executa query simples para verificar conexão
        print("Conexão com o banco OK")
    finally:
        db.close() # Fecha sessão