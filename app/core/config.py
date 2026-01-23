from pydantic_settings import BaseSettings

# Configurações da aplicação via Pydantic

class Settings(BaseSettings):
    app_name: str = "PedidoFácil Backend" # Nome da aplicação
    environment: str = "local" # Ambiente atual
    debug: bool = True # Habilita modo de depuração

    class Config:
        env_file = ".env" # Arquivo de variáveis de ambiente

# Instância das configurações
settings = Settings()