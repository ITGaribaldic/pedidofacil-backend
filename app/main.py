from fastapi import FastAPI
from app.core.config import settings       # Configurações da aplicação
from app.core.logger_config import logger  # Logger global
from app.api.routes.health import router as health_router # Router de health check
from app.api.routes.users import router as users_router
from app.api.routes import auth

# Log de inicialização da aplicação
logger.info(f"Aplicação {settings.app_name} iniciada no ambiente {settings.environment}")

# Cria instância da aplicação FastAPI
app = FastAPI(title=settings.app_name)

# R Registra routers na aplicação
app.include_router(health_router)
app.include_router(users_router)  # registra o router de usuários
app.include_router(auth.router)