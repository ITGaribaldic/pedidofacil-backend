from pydantic_settings import BaseSettings

# Classe de configuração da aplicação usando Pydantic
class Settings(BaseSettings):
    # Nome da aplicação
    app_name: str = "PedidoFácil Backend"
    # Ambiente de execução (local, dev, prod)
    environment: str = "local"
    # Flag para habilitar debug
    debug: bool = True

    class Config:
        # Arquivo .env para variáveis de ambiente
        env_file = ".env"

# Instância das configurações que será importada em outros módulos
settings = Settings()