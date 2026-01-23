from app.core.database import SessionLocal
from app.core.models.user import User
from app.core.models.client import Client
from app.core.models.product import Product
from app.core.models.order import Order

def test_user_crud(db):
    # CREATE
    user = User(
        email="teste@email.com",
        username="teste",
        full_name="Usuario Teste"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    print("USER CREATE OK", user.id)

    # READ
    user_db = db.query(User).filter(User.email == "teste@email.com").first()
    print("USER READ OK", user_db.email if user_db else None)

    # UPDATE
    if user_db:
        user_db.full_name = "Usuario Atualizado"  # type: ignore
        db.commit()
        db.refresh(user_db)
        print("USER UPDATE OK", user_db.full_name if user_db else None)

    # DELETE
    if user_db:
        db.delete(user_db)
        db.commit()
        print("USER DELETE OK")

def test_client_crud(db):
    client = Client(
        name="Cliente Teste",
        email="cliente@teste.com",
        phone="123456789",
        adress="Rua Teste, 123"
    )
    db.add(client)
    db.commit()
    db.refresh(client)
    print("CLIENT CREATE OK", client.id)

    client_db = db.query(Client).filter(Client.email == "cliente@teste.com").first()
    print("CLIENT READ OK", client_db.email if client_db else None)

    if client_db:
        client_db.name = "Cliente Atualizado"  # type: ignore
        db.commit()
        db.refresh(client_db)
        print("CLIENT UPDATE OK", client_db.name if client_db else None)

    if client_db:
        db.delete(client_db)
        db.commit()
        print("CLIENT DELETE OK")

def test_product_crud(db):
    product = Product(
        name="Produto Teste",
        description="Produto para teste",
        price=100.0,
        stock=10
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    print("PRODUCT CREATE OK", product.id)

    product_db = db.query(Product).filter(Product.name == "Produto Teste").first()
    print("PRODUCT READ OK", product_db.name if product_db else None)

    if product_db:
        product_db.price = 120.0  # type: ignore
        db.commit()
        db.refresh(product_db)
        print("PRODUCT UPDATE OK", product_db.price if product_db else None)

    if product_db:
        db.delete(product_db)
        db.commit()
        print("PRODUCT DELETE OK")

def test_order_crud(db):
    # Criar Client e Product para o Order
    client = Client(name="Cliente Pedido", email="pedido@teste.com")  # type: ignore
    product = Product(name="Produto Pedido", price=50.0)  # type: ignore
    db.add_all([client, product])
    db.commit()
    db.refresh(client)
    db.refresh(product)

    order = Order(
        client_id=client.id,
        product_id=product.id,
        quantity=2,
        total_price=100.0
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    print("ORDER CREATE OK", order.id)

    order_db = db.query(Order).filter(Order.id == order.id).first()
    print("ORDER READ OK", order_db.id if order_db else None)

    if order_db:
        order_db.quantity = 3  # type: ignore
        order_db.total_price = 150.0  # type: ignore
        db.commit()
        db.refresh(order_db)
        print("ORDER UPDATE OK", order_db.quantity if order_db else None, order_db.total_price if order_db else None)

    # DELETE
    db.delete(order)
    db.delete(client)
    db.delete(product)
    db.commit()
    print("ORDER DELETE OK")


if __name__ == "__main__":
    db = SessionLocal()
    try:
        test_user_crud(db)
        test_client_crud(db)
        test_product_crud(db)
        test_order_crud(db)
    finally:
        db.close()