from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
# Importa a base do SQLAlchemy e todos os modelos para que o Alembic possa detectar metadados
from app.core.models.base import Base
import app.core.models
# Configuração do Alembic
config = context.config
# Configura logging se existir arquivo de configuração
if config.config_file_name is not None:
    fileConfig(config.config_file_name)
# Metadata usada pelo Alembic para autogerar migrations
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Executa migrations em modo offline.

    Neste modo, o Alembic gera SQL diretamente sem se conectar ao banco.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, # URL do banco de dados
        target_metadata=target_metadata, # Metadados das tabelas
        literal_binds=True,# Gera valores literais no SQL
        dialect_opts={"paramstyle": "named"}, # Estilo de parâmetros compatível com SQLAlchemy
    )

    with context.begin_transaction():
        context.run_migrations() # Executa as migrations


def run_migrations_online() -> None:
    """Executa migrations em modo online.

    Neste modo, o Alembic conecta-se ao banco e aplica as alterações diretamente.
    """
    # Cria engine de conexão usando as configurações do arquivo alembic.ini
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool, # Desativa pool para evitar conexões persistentes
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, # Conexão ativa
            target_metadata=target_metadata, # Metadados das tabelas
        )

        with context.begin_transaction():
            context.run_migrations() # Executa as migrations

# Executa a função adequada dependendo do modo offline/online
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()