from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional, Tuple
from datetime import datetime

from app.core.models import Order, OrderItem, OrderStatus, Product, Client
from app.schemas.order import OrderCreate, OrderUpdate
from app.services.exceptions import NotFoundException, BusinessRuleException


class OrderService:

    @staticmethod
    def _get_product_id(product) -> int:
        # Extrai o id do produto mesmo quando o objeto não é uma instância completa do modelo
        try:
            if hasattr(product, "id"):
                pid = product.id
                if hasattr(pid, "__int__"):
                    return int(pid)
                if isinstance(pid, (int, float)):
                    return int(pid)
                return getattr(product, "_id", 0)
            return 0
        except Exception:
            return 0

    @staticmethod
    def _get_client_id(client) -> int:
        # Garante a obtenção do id do cliente de forma segura
        try:
            if hasattr(client, "id"):
                cid = client.id
                if hasattr(cid, "__int__"):
                    return int(cid)
                if isinstance(cid, (int, float)):
                    return int(cid)
            return 0
        except Exception:
            return 0

    @staticmethod
    def create_order(db: Session, order_data: OrderCreate, current_user_id: int) -> Order:
        # Valida se o cliente pertence ao usuário autenticado
        client = db.query(Client).filter(
            Client.id == order_data.client_id,
            Client.user_id == current_user_id
        ).first()

        if not client:
            raise NotFoundException("Cliente não encontrado ou não pertence ao usuário")

        product_ids = [item.product_id for item in order_data.items]

        # Carrega apenas dados necessários para cálculo do pedido
        products = db.query(Product.id, Product.name, Product.price).filter(
            Product.id.in_(product_ids)
        ).all()

        # Garante que todos os produtos informados existem
        if len(products) != len(product_ids):
            found_ids = []
            for p in products:
                pid = p[0] if isinstance(p, tuple) else OrderService._get_product_id(p)
                found_ids.append(pid)

            missing_ids = [pid for pid in product_ids if pid not in found_ids]
            raise NotFoundException(f"Produtos não encontrados: {missing_ids}")

        order = Order(
            client_id=order_data.client_id,
            status=OrderStatus.PENDING.value
        )
        db.add(order)
        db.flush()

        # Mapa auxiliar para acesso rápido aos dados do produto
        product_map = {}
        for p in products:
            if isinstance(p, tuple):
                pid, pname, pprice = p
                product_map[pid] = {
                    "id": pid,
                    "name": pname,
                    "price": pprice,
                    "stock": 0
                }
            else:
                pid = OrderService._get_product_id(p)
                product_map[pid] = {
                    "id": pid,
                    "name": p.name if hasattr(p, "name") else "",
                    "price": p.price if hasattr(p, "price") else 0.0,
                    "stock": p.stock if hasattr(p, "stock") else 0
                }

        total = 0.0

        for item_data in order_data.items:
            product_info = product_map.get(item_data.product_id)
            if not product_info:
                raise NotFoundException(f"Produto ID {item_data.product_id} não encontrado")

            # Regra de estoque aplicada apenas quando disponível no modelo
            if product_info["stock"] < item_data.quantity:
                raise BusinessRuleException(
                    f"Estoque insuficiente para produto '{product_info['name']}'. "
                    f"Disponível: {product_info['stock']}, Solicitado: {item_data.quantity}"
                )

            unit_price = product_info["price"]
            subtotal = unit_price * item_data.quantity

            order_item = OrderItem(
                order_id=order.id,
                product_id=item_data.product_id,
                quantity=item_data.quantity,
                unit_price=unit_price,
                subtotal=subtotal
            )
            db.add(order_item)
            total += subtotal

        order.total = total
        db.commit()
        db.refresh(order)

        return order

    @staticmethod
    def get_orders(
        db: Session,
        current_user_id: int,
        client_id: Optional[int] = None,
        status: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        skip: int = 0,
        limit: int = 100
    ) -> Tuple[List[Order], int]:
        query = db.query(Order).join(Order.client).filter(Client.user_id == current_user_id)

        if client_id:
            query = query.filter(Order.client_id == client_id)

        if status:
            query = query.filter(Order.status == status)

        if start_date:
            query = query.filter(Order.created_at >= start_date)

        if end_date:
            query = query.filter(Order.created_at <= end_date)

        total = query.count()

        orders = query.order_by(desc(Order.created_at)).offset(skip).limit(limit).all()

        return orders, total

    @staticmethod
    def get_order_by_id(db: Session, order_id: int, current_user_id: int) -> Order:
        order = db.query(Order).join(Order.client).filter(
            Order.id == order_id,
            Client.user_id == current_user_id
        ).first()

        if not order:
            raise NotFoundException("Pedido não encontrado")

        # Garante que atributos principais estejam carregados antes do retorno
        _ = order.id
        _ = order.status
        _ = order.total

        return order

    @staticmethod
    def update_order_status(
        db: Session,
        order_id: int,
        status_update: OrderUpdate,
        current_user_id: int
    ) -> Order:
        order = OrderService.get_order_by_id(db, order_id, current_user_id)

        if not status_update.status:
            return order

        new_status = status_update.status.value

        # Define transições válidas do fluxo do pedido
        valid_transitions = {
            OrderStatus.PENDING.value: [
                OrderStatus.CONFIRMED.value,
                OrderStatus.CANCELLED.value
            ],
            OrderStatus.CONFIRMED.value: [
                OrderStatus.PROCESSING.value,
                OrderStatus.CANCELLED.value
            ],
            OrderStatus.PROCESSING.value: [
                OrderStatus.SHIPPED.value,
                OrderStatus.CANCELLED.value
            ],
            OrderStatus.SHIPPED.value: [OrderStatus.DELIVERED.value],
            OrderStatus.DELIVERED.value: [],
            OrderStatus.CANCELLED.value: []
        }

        current_status = (
            str(order.status)
            if order.status is not None
            else OrderStatus.PENDING.value
        )

        allowed_next = valid_transitions.get(current_status, [])

        if new_status not in allowed_next:
            raise BusinessRuleException(
                f"Transição inválida de '{current_status}' para '{new_status}'. "
                f"Transições permitidas: {allowed_next}"
            )

        setattr(order, "status", new_status)
        db.commit()
        db.refresh(order)

        return order

    @staticmethod
    def delete_order(db: Session, order_id: int, current_user_id: int) -> bool:
        order = OrderService.get_order_by_id(db, order_id, current_user_id)

        order_status = (
            str(order.status)
            if order.status is not None
            else OrderStatus.PENDING.value
        )

        # Exclusão permitida apenas enquanto o pedido está pendente
        if order_status != OrderStatus.PENDING.value:
            raise BusinessRuleException(
                f"Não é possível excluir um pedido com status '{order_status}'. "
                "Apenas pedidos pendentes podem ser excluídos."
            )

        db.delete(order)
        db.commit()

        return True
