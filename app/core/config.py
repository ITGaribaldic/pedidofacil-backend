from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "PedidoFácil Backend"
    environment: str = "local"
    debug: bool = True

    class Config:
        env_file = ".env"

settings = Settings()