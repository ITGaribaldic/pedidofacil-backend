from fastapi import FastAPI
from app.core.config import settings
from app.core.logger_config import logger
from app.api.routes.health import router as health_router
from app.api.routes.users import router as users_router
from app.api.routes.auth import router as auth_router
from app.api.routes.clients import router as clients_router
from app.api.routes.products import router as products_router


# Log de inicialização da aplicação
logger.info(f"Aplicação {settings.app_name} iniciada no ambiente {settings.environment}")

# Cria instância da aplicação FastAPI
app = FastAPI(title=settings.app_name)

# Registra routers na aplicação
app.include_router(health_router)
app.include_router(users_router)
app.include_router(auth_router)
app.include_router(clients_router)
app.include_router(products_router)