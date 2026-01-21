from fastapi import FastAPI
from app.core.config import settings  # Importa as configurações centralizadas
from app.api.routes.health import router as health_router  # Importa router do health

# Criação da aplicação FastAPI com título vindo das configurações
app = FastAPI(title=settings.app_name)

# Registro dos routers da aplicação
# Permite separar responsabilidades e manter o main.py limpo
app.include_router(health_router)