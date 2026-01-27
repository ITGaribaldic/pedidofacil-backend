from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user import UserCreate,UserRead
from app.core.security import get_password_hash
from app.core.models.user import User
from app.core.dependencies import get_current_user

router = APIRouter(
    prefix = "/users",
    tags= ["users"]
)

@router.post("/", response_model=UserRead)
def create_user(user: UserCreate,db: Session = Depends(get_db)):
    # verifica se o email já existe
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail= "Email já cadastrado")
    
    # Cria usuário com senha hash
    hashed_password = get_password_hash(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        password_hash=hashed_password
    )


    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/me", response_model=UserRead)
def read_current_user(
    current_user: User = Depends(get_current_user)
):
    return current_user