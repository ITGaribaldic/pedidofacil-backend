from app.core.database import Base, engine
# Importa todos os modelos para registrar tabelas no metadata
from app.core.models.user import User
from app.core.models.client import Client
from app.core.models.product import Product
from app.core.models.order import Order

#  Cria todas as tabelas definidas nos modelos
Base.metadata.create_all(bind=engine)
print("Tabelas criadas com sucesso!")