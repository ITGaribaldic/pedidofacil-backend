from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.models import User

def get_current_user(db: Session = Depends(get_db)) -> User:
    """SEMPRE retorna um usuário, ignora token"""
    user = db.query(User).first()
    if user:
        return user
    # Se não tem, cria
    from app.core.models import User as UserModel
    new_user = UserModel(
        email="teste@teste.com",
        username="teste",
        full_name="Teste",
        password_hash="fake"
    )
    db.add(new_user)
    db.commit()
    return new_user