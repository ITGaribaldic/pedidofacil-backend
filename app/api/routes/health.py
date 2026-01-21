from fastapi import APIRouter
from app.core.logger_config import logger  # Usa logger global

# Criar router específico para rotas relacionadas à saúde da API
router = APIRouter()

# Endpoint GET /health
@router.get("/health")
def health_check():
    """
    Retorna status da aplicação.
    Pode ser usado para monitoramento ou verificação rápida.
    """
    logger.info("Endpoint /health acessado")
    return {"status": "ok"}