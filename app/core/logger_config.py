import logging
# Configuração global do logging
logging.basicConfig(
    level=logging.INFO, # Nível de log padrão
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s" # Formato das mensagens
)

# Logger principal da aplicação
logger = logging.getLogger("pedidofacil")