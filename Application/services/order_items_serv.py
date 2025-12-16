from sqlalchemy.ext.asyncio import AsyncSession

from Application.repositories.products_rep import get_product
from Application.schemas import OrderItemsCreate
from Application.services.orders_serv import check_user_order
from Application.repositories.order_items_rep import (
    get_order_items,
    get_orders_items,
    create_order_items,
    del_order_item,
)


async def check_user_items(session: AsyncSession, user_id: int, order_id: int):
    order = await check_user_order(session, user_id, order_id)
    items = await get_orders_items(session)
    result = []
    if order:
        for item in items:
            if item.order_id == order_id:
                result.append(item)
        if result:
            return result
        raise ValueError("Товары не найдены")
    raise ValueError("Заказ не найден")


async def check_user_item(
    session: AsyncSession, user_id: int, order_id: int, item_id: int
):
    order = await check_user_order(session, user_id, order_id)
    items = await check_user_items(session, user_id, order_id)
    if not order:
        raise ValueError("Заказ не найден")
    if items:
        for item in items:
            if item.order_item_id == item_id:
                return item
            raise ValueError("Товар не найден")
    raise ValueError("Товар не найден")


async def check_items(session: AsyncSession):
    items = await get_orders_items(session)
    if items:
        return items
    raise ValueError("Товары не найдены")


async def check_item(session: AsyncSession, order_items_id: int):
    item = await get_order_items(session, order_items_id)
    if item:
        return item
    raise ValueError("Товар не найден")


async def add_order_item(
    session: AsyncSession, user_id: int, order_item_data: OrderItemsCreate
):
    order = await check_user_order(session, user_id, order_item_data.order_id)
    product = await get_product(session, order_item_data.product_id)
    if not order:
        raise ValueError("Заказ не найден")
    elif not product:
        raise ValueError("Товар не найден")
    elif order.status == "on the way":
        await create_order_items(session, order_item_data)
    else:
        raise ValueError("Заказ не может быть изменён")


async def remove_order_item(
    session: AsyncSession, item_id: int, user_id: int, order_id: int
):
    await del_order_item(session, item_id)
    order = await check_user_order(session, user_id, order_id)
    if order and order.status == "on the way":
        item = await get_order_items(session, item_id)
        if item:
            await del_order_item(session, item_id)
        else:
            raise ValueError("Товар не найден")
    else:
        raise ValueError("Заказ не найден")
