from pydantic_settings import BaseSettings

# Configurações da aplicação via Pydantic

class Settings(BaseSettings):
    app_name: str = "PedidoFácil Backend"
    environment: str = "local"
    debug: bool = True

    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    class Config:
        env_file = ".env"

# Instância das configurações
settings = Settings()