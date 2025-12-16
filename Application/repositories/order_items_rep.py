from sqlalchemy import select
from Application.models import OrderItemsORM
from Application.schemas import OrderItemsCreate
from sqlalchemy.ext.asyncio import AsyncSession


async def get_orders_items(session: AsyncSession):
    query = select(OrderItemsORM)
    result = await session.execute(query)
    return result.scalars().all()


async def get_order_items(session: AsyncSession, order_items_id: int):
    order_items = await session.get(OrderItemsORM, order_items_id)
    return order_items


async def create_order_items(session: AsyncSession, order_items_data: OrderItemsCreate):
    order_items = OrderItemsORM(
        order_id=order_items_data.order_id,
        product_id=order_items_data.product_id,
        quantity=order_items_data.quantity,
    )
    session.add(order_items)


async def del_order_item(session: AsyncSession, order_items_id: int):
    order_items = await get_order_items(session, order_items_id)
    await session.delete(order_items)
