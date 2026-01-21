from fastapi import APIRouter

# Criar router específico para rotas relacionadas à saúde da API
router = APIRouter()

# Endpoint GET /health
@router.get("/health")
def health_check():
    """
    Retorna status da aplicação.
    Pode ser usado para monitoramento ou verificação rápida.
    """
    return {"status": "ok"}