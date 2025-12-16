from sqlalchemy.ext.asyncio import AsyncSession
from Application.repositories.orders_rep import (
    get_order,
    get_orders,
    del_order,
    update_status,
    get_user_orders,
    create_order,
)
from Application.schemas import OrdersCreate


async def check_orders(session: AsyncSession):
    orders = await get_orders(session)
    if orders:
        return orders
    raise ValueError("Заказы не найдены")


async def check_order(session: AsyncSession, order_id: int):
    order = await get_order(session, order_id)
    if order:
        return order
    raise ValueError("Заказ не найдены")


async def check_user_orders(session: AsyncSession, user_id: int):
    orders = await get_user_orders(session, user_id)
    if orders:
        return orders
    raise ValueError("Заказы не найдены")


async def check_user_order(session: AsyncSession, user_id: int, order_id: int):
    orders = await get_user_orders(session, user_id)
    for order in orders:
        if order.order_id == order_id:
            return order
    raise ValueError("Заказ не найден")


async def add_order(session: AsyncSession, user_id: int):
    await create_order(session, user_id, "on the way")


async def change_status(session: AsyncSession, order_id: int):
    order = await get_order(session, order_id)
    if order:
        if order.status == "on the way":
            await update_status(session, order_id, "delivered")
            return {"status": "Заказ доставлен"}
        elif order.status == "delivered":
            await update_status(session, order_id, "received")
            return {"status": "Заказ отдан"}
    else:
        ValueError("Заказ не найден")


async def remove_order(session: AsyncSession, order_id: int):
    order = await get_order(session, order_id)
    if order:
        await del_order(session, order_id)
    else:
        ValueError("Заказ не найден")
