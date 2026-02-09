from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logger_config import logger
from app.api.routes.health import router as health_router
from app.api.routes.users import router as users_router
from app.api.routes.auth import router as auth_router
from app.api.routes.clients import router as clients_router
from app.api.routes.products import router as products_router
from app.api.routes.orders import router as orders_router

logger.info(f"Aplicação {settings.app_name} iniciada no ambiente {settings.environment}")

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # liberar apenas em desenvolvimento
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(users_router)
app.include_router(auth_router)
app.include_router(clients_router)
app.include_router(products_router)
app.include_router(orders_router)