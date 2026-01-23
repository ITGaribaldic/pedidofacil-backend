from app.core.database import Base, engine
# Importar todos os modelos para que Base conheça as tabelas
from app.core.models.user import User
from app.core.models.client import Client
from app.core.models.product import Product
from app.core.models.order import Order

# Criar todas as tabelas no banco
Base.metadata.create_all(bind=engine)
print("Tabelas criadas com sucesso!")