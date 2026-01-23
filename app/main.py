from fastapi import FastAPI
from app.core.config import settings       # Importa configurações
from app.core.logger_config import logger  # Importa logger global
from app.api.routes.health import router as health_router

# Log de inicialização da aplicação
logger.info(f"Aplicação {settings.app_name} iniciada no ambiente {settings.environment}")

# Criação da aplicação FastAPI
app = FastAPI(title=settings.app_name)

# Registro dos routers da aplicação
app.include_router(health_router)