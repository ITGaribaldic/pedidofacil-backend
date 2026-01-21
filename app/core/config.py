from pydantic_settings import BaseSettings

# Classe de configuração da aplicação usando Pydantic
class Settings(BaseSettings):
    app_name: str = "PedidoFácil Backend"
    environment: str = "local"
    debug: bool = True

    class Config:
        env_file = ".env"

# Instância das configurações
settings = Settings()