"""Descricao da migration

Revision ID: 29b138bb7da7
Revises: fd5b94cab3b6
Create Date: 2026-01-22 21:44:28.655145

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# Identificadores da migration usados pelo Alembic
revision: str = '29b138bb7da7'
down_revision: Union[str, Sequence[str], None] = 'fd5b94cab3b6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Executa alterações para atualizar o schema do banco de dados.
    
    Adicione aqui os comandos de criação/alteração de tabelas, colunas, índices, etc.
    """
    # ### comandos gerados automaticamente pelo Alembic - ajuste conforme necessário ###
    pass
    # ### fim dos comandos Alembic ###


def downgrade() -> None:
    """Reverte alterações aplicadas pelo método upgrade.
    
    Adicione aqui os comandos para desfazer as alterações feitas na migration.
    """
    # ### comandos gerados automaticamente pelo Alembic - ajuste conforme necessário ###
    pass
    # ### fim dos comandos Alembic ###