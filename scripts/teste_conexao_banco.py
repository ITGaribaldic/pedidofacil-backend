from app.core.database import SessionLocal
from sqlalchemy import text
def test_connection():
    db = SessionLocal()
    try:
        db.execute(text("SELECT 1"))
        print("Conexão com o banco OK")
    finally:
        db.close()