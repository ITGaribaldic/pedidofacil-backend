"""Initial migration

Revision ID: fd5b94cab3b6
Revises: 
Create Date: 2026-01-22 17:42:26.174968

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# Identificadores da migration usados pelo Alembic
revision: str = 'fd5b94cab3b6'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Executa alterações para atualizar o schema do banco de dados.

    Neste caso, esta migration inicial remove tabelas e índices existentes
    (se houver) para garantir que o banco comece em um estado limpo.
    """
    # Remover tabela de pedidos
    op.drop_table('orders')
    # Remover índice da tabela products
    op.drop_index(op.f('ix_products_id'), table_name='products')
    # Remover tabela de produtos
    op.drop_table('products')
    # Remover índice da tabela clients
    op.drop_index(op.f('ix_clients_id'), table_name='clients')
    # Remover tabela de clientes
    op.drop_table('clients')
    # Remover índice da tabela users
    op.drop_index(op.f('ix_users_id'), table_name='users')
    # Remover tabela de usuários
    op.drop_table('users')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Reverte alterações aplicadas pelo método upgrade.

    Neste caso, recria todas as tabelas removidas no upgrade, incluindo
    colunas, chaves primárias, únicas e relações de chave estrangeira.
    """
    # Recriar tabela de usuários
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('username', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('email', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('full_name', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('users_pkey')),
    sa.UniqueConstraint('email', name=op.f('users_email_key'), postgresql_include=[], postgresql_nulls_not_distinct=False),
    sa.UniqueConstraint('username', name=op.f('users_username_key'), postgresql_include=[], postgresql_nulls_not_distinct=False)
    )
    # Criar índice de id na tabela users
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    # Recriar tabela de clientes
    op.create_table('clients',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('phone', sa.VARCHAR(length=20), autoincrement=False, nullable=True),
    sa.Column('adress', sa.VARCHAR(length=200), autoincrement=False, nullable=True),
    sa.Column('creadet_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.Column('active', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('clients_pkey')),
    sa.UniqueConstraint('email', name=op.f('clients_email_key'), postgresql_include=[], postgresql_nulls_not_distinct=False)
    )
    # Criar índice de id na tabela clients
    op.create_index(op.f('ix_clients_id'), 'clients', ['id'], unique=False)
    op.create_table('products',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('description', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('price', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.Column('stock', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('products_pkey'))
    )
    # Criar índice de id na tabela products
    op.create_index(op.f('ix_products_id'), 'products', ['id'], unique=False)
    # Recriar tabela de pedidos

    op.create_table('orders',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('client_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('product_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('quantity', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('total_price', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.Column('completed', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['client_id'], ['clients.id'], name=op.f('orders_client_id_fkey')),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], name=op.f('orders_product_id_fkey')),
    sa.PrimaryKeyConstraint('id', name=op.f('orders_pkey'))
    )
    # ### end Alembic commands ###
