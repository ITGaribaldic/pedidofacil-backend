import os
import secrets
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Diretório onde este arquivo config.py está
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Carrega o .env da mesma pasta
load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env"))

class Settings(BaseSettings):
    app_name: str = "PedidoFácil Backend"
    environment: str = "local"
    debug: bool = True

    # Aqui garantimos que o valor vem do ambiente ou geramos um default
    secret_key: str = os.environ.get("SECRET_KEY", secrets.token_urlsafe(32))
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    class Config:
        env_file = os.path.join(BASE_DIR, ".env")
        # Pydantic vai sobrescrever secret_key se estiver no .env

# Instancia as configurações
settings = Settings()

print("Chave secreta:", settings.secret_key)
