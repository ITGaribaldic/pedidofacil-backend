import logging

# Configuração global do logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

# Logger global que será importado por todos os módulos
logger = logging.getLogger("pedidofacil")