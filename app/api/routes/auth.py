from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.models.user import User
from app.core.security import verify_password, create_access_token
from fastapi.security import OAuth2PasswordRequestForm

# Cria um router FastAPI para endpoints de autenticação
router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),  # Recebe username e password via form-urlencoded
    db: Session = Depends(get_db),                     # Injeção de dependência do banco de dados
):
    """
    Endpoint para autenticação de usuários.
    
    Recebe email (username) e senha, verifica se as credenciais estão corretas
    e retorna um JWT Bearer token válido para acesso aos endpoints protegidos.
    """
    # Busca usuário pelo email fornecido no form
    db_user = db.query(User).filter(User.email == form_data.username).first()

    # Valida se usuário existe e senha está correta
    if not db_user or not verify_password(form_data.password, db_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",  # Mensagem amigável sem expor detalhes de segurança
        )

    # Gera token JWT contendo o ID do usuário como "sub"
    access_token = create_access_token(
        data={"sub": str(db_user.id)}
    )

    # Retorna token e tipo Bearer
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
