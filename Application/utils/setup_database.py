from Application.core.connection import Base, engine
from Application.core.connection import session
from Application.models import *

async def setup_db():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)

    async with session.begin() as sess:
        user1 = UsersORM(
            firstname="Alice",
            lastname="Smith",
            email="alice@example.com",
            password_hash="hashed_pw1",
            role="user",
            is_active=True
        )
        user2 = UsersORM(
            firstname="Bob",
            lastname="Johnson",
            email="bob@example.com",
            password_hash="hashed_pw2",
            role="user",
            is_active=True
        )

        sess.add_all([user1, user2])
        await sess.flush()


        product1 = ProductsORM(name="Laptop", category="Electronics", price=1200.0)
        product2 = ProductsORM(name="Mouse", category="Electronics", price=25.0)
        product3 = ProductsORM(name="Chair", category="Furniture", price=150.0)

        sess.add_all([product1, product2, product3])
        await sess.flush()


        order1 = OrdersORM(user_id=user1.user_id, status="on the way")
        order2 = OrdersORM(user_id=user2.user_id, status="delivered")
        order3 = OrdersORM(user_id=user1.user_id, status="received")

        sess.add_all([order1, order2, order3])
        await sess.flush()

        item1 = OrderItemsORM(order_id=order1.order_id, product_id=product1.product_id, quantity=1)
        item2 = OrderItemsORM(order_id=order1.order_id, product_id=product2.product_id, quantity=2)
        item3 = OrderItemsORM(order_id=order2.order_id, product_id=product3.product_id, quantity=1)
        item4 = OrderItemsORM(order_id=order3.order_id, product_id=product2.product_id, quantity=3)

        sess.add_all([item1, item2, item3, item4])

        await sess.commit()
