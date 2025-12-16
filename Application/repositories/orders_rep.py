from sqlalchemy import select
from Application.models import OrdersORM
from Application.schemas import OrdersCreate
from sqlalchemy.ext.asyncio import AsyncSession


async def get_orders(session: AsyncSession):
    query = select(OrdersORM)
    result = await session.execute(query)
    return result.scalars().all()


async def get_order(session: AsyncSession, order_id: int):
    order = await session.get(OrdersORM, order_id)
    return order


async def get_user_orders(session: AsyncSession, user_id):
    query = select(OrdersORM).where(OrdersORM.user_id == user_id)
    result = await session.execute(query)
    return result.scalars().all()


async def create_order(session: AsyncSession, user_id: int, status: str):
    order = OrdersORM(user_id=user_id, status=status)
    session.add(order)


async def del_order(session: AsyncSession, order_id: int):
    order = await get_order(session, order_id)
    await session.delete(order)


async def update_status(session: AsyncSession, order_id: int, status: str):
    order = await get_order(session, order_id)
    order.status = status
