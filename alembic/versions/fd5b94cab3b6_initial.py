from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# Metadados da migração
revision: str = "fd5b94cab3b6"  # Identificador único desta migração
down_revision: Union[str, Sequence[str], None] = None  # Esta é a primeira migração
branch_labels: Union[str, Sequence[str], None] = None  # Sem branches específicos
depends_on: Union[str, Sequence[str], None] = None  # Sem dependências externas

def upgrade() -> None:
    # Criação da tabela 'users' para armazenamento de usuários do sistema
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("username", sa.String(length=50), nullable=True, unique=True),
        sa.Column("email", sa.String(length=100), nullable=False, unique=True),
        sa.Column("full_name", sa.String(length=100), nullable=True),
        sa.Column("password_hash", sa.String(length=128), nullable=False),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(),
            server_default=sa.text("now()"),  # Define timestamp atual por padrão
            nullable=False,
        ),
    )

    # Tabela 'clients' para armazenar informações dos clientes
    op.create_table(
        "clients",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=100), nullable=False, unique=True),
        sa.Column("phone", sa.String(length=20), nullable=True),
        sa.Column("address", sa.String(length=200), nullable=True),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "active",
            sa.Boolean(),
            server_default=sa.text("true"),  # Cliente ativo por padrão
            nullable=False,
        ),
    )

    # Tabela 'products' para cadastro de produtos
    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.Column("price", sa.Numeric(10, 2), nullable=False),  # Precisão: 10 dígitos, 2 decimais
        sa.Column("stock", sa.Integer(), nullable=True),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )

    # Tabela 'orders' para registro de pedidos
    op.create_table(
        "orders",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "client_id",
            sa.Integer(),
            sa.ForeignKey("clients.id", ondelete="RESTRICT"),  # Impede exclusão se houver pedidos
            nullable=False,
        ),
        sa.Column("total_price", sa.Numeric(12, 2), nullable=False),  # Maior precisão para valores totais
        sa.Column(
            "status",
            sa.String(length=20),
            server_default=sa.text("'pending'"),  # Status inicial padrão
            nullable=False,
        ),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            postgresql.TIMESTAMP(),
            server_default=sa.text("now()"),  # Atualização automática via trigger recomendada
            nullable=False,
        ),
    )

    # Tabela 'order_items' para itens individuais dos pedidos
    op.create_table(
        "order_items",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "order_id",
            sa.Integer(),
            sa.ForeignKey("orders.id", ondelete="CASCADE"),  # Itens excluídos com o pedido
            nullable=False,
        ),
        sa.Column(
            "product_id",
            sa.Integer(),
            sa.ForeignKey("products.id", ondelete="RESTRICT"),  # Impede exclusão de produto em uso
            nullable=False,
        ),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("unit_price", sa.Numeric(10, 2), nullable=False),  # Preço no momento da compra
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        # Constraint única para evitar duplicação de produtos no mesmo pedido
        sa.UniqueConstraint(
            "order_id",
            "product_id",
            name="uq_order_items_order_product",
        ),
    )

    # Índices para otimização de consultas
    op.create_index("ix_clients_name", "clients", ["name"])
    op.create_index("ix_products_name", "products", ["name"])
    op.create_index("ix_orders_created_at", "orders", ["created_at"])  # Útil para relatórios temporais
    op.create_index("ix_orders_status", "orders", ["status"])  # Filtragem por status
    op.create_index("ix_order_items_order_id", "order_items", ["order_id"])
    op.create_index("ix_order_items_product_id", "order_items", ["product_id"])

def downgrade() -> None:
    # Ordem inversa: índices primeiro, tabelas depois
    op.drop_index("ix_order_items_product_id", table_name="order_items")
    op.drop_index("ix_order_items_order_id", table_name="order_items")
    op.drop_index("ix_orders_status", table_name="orders")
    op.drop_index("ix_orders_created_at", table_name="orders")
    op.drop_index("ix_products_name", table_name="products")
    op.drop_index("ix_clients_name", table_name="clients")

    # Remoção das tabelas na ordem inversa da criação
    op.drop_table("order_items")
    op.drop_table("orders")
    op.drop_table("products")
    op.drop_table("clients")
    op.drop_table("users")