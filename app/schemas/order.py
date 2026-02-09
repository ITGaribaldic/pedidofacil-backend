from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict
from enum import Enum


class OrderStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class OrderItemBase(BaseModel):
    # Campos comuns usados em criação e retorno de itens
    product_id: int = Field(..., gt=0, description="ID do produto")
    quantity: int = Field(..., gt=0, description="Quantidade deve ser maior que zero")
    unit_price: float = Field(..., gt=0, description="Preço unitário deve ser positivo")


class OrderItemCreate(OrderItemBase):
    # Schema usado exclusivamente na criação do pedido
    product_id: int = Field(..., gt=0, description="ID do produto")
    quantity: int = Field(..., gt=0, description="Quantidade deve ser maior que zero")


class OrderItem(OrderItemBase):
    # Representa item persistido e retornado pela API
    model_config = ConfigDict(from_attributes=True)

    id: int
    order_id: int
    subtotal: float = Field(..., description="Quantidade x preço unitário")

    @field_validator("subtotal")
    @classmethod
    def validate_subtotal(cls, v: float, info):
        # Garante consistência entre subtotal, quantidade e preço
        data = info.data
        if "quantity" in data and "unit_price" in data:
            expected = data["quantity"] * data["unit_price"]
            if abs(v - expected) > 0.01:
                raise ValueError(
                    f"Subtotal incorreto. Esperado: {expected:.2f}, Recebido: {v:.2f}"
                )
        return v


class OrderBase(BaseModel):
    # Campos básicos compartilhados entre schemas de pedido
    client_id: int = Field(..., gt=0, description="ID do cliente")
    status: OrderStatus = Field(
        default=OrderStatus.PENDING,
        description="Status do pedido"
    )


class OrderCreate(BaseModel):
    # Usado apenas na criação de pedidos
    client_id: int = Field(..., gt=0, description="ID do cliente")
    items: List[OrderItemCreate] = Field(
        min_length=1,
        description="Lista de itens do pedido"
    )

    @field_validator("items")
    @classmethod
    def validate_items_unique(cls, v: List[OrderItemCreate]):
        # Impede o mesmo produto mais de uma vez no pedido
        product_ids = [item.product_id for item in v]
        if len(product_ids) != len(set(product_ids)):
            raise ValueError(
                "Não é permitido repetir o mesmo produto nos itens"
            )
        return v


class OrderUpdate(BaseModel):
    # Atualização parcial permitida apenas para status
    status: Optional[OrderStatus] = None


class Order(BaseModel):
    # Representação padrão do pedido retornado pela API
    model_config = ConfigDict(from_attributes=True)

    id: int
    client_id: int
    status: OrderStatus
    total: float = Field(..., ge=0, description="Total do pedido")
    created_at: datetime
    updated_at: datetime


class OrderWithItems(Order):
    # Versão expandida do pedido com seus itens
    items: List[OrderItem] = Field(
        default_factory=list,
        description="Itens do pedido"
    )
