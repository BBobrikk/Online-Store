from sqlalchemy.ext.asyncio import AsyncSession
from Application.repositories.products_rep import (
    get_product,
    get_products,
    del_product,
    create_product,
    update_product,
    get_product_by_name,
)
from Application.schemas import ProductsCreate, ProductsUpdate


async def check_products(session: AsyncSession):
    products = await get_products(session)
    if products:
        return products
    raise ValueError("Товары не найдены")


async def check_product(session: AsyncSession, product_id):
    product = await get_product(session, product_id)
    if product:
        return product
    raise ValueError("Товар не найден")


async def add_product(session: AsyncSession, product_data: ProductsCreate):
    product = await get_product_by_name(session, product_data.name)
    if product:
        raise ValueError("Такой товар уже существует")
    await create_product(session, product_data)


async def update_product_serv(
    session: AsyncSession, product_data: ProductsUpdate, product_id: int
):
    products = await get_products(session)
    for product in products:
        if product.product_id == product_id and product.name == product_data.name:
            await update_product(session, product_data, product_id)
        elif product.product_id == product_id and product.name != product_data.name:
            await update_product(session, product_data, product_id)
        elif product.product_id != product_id and product.name == product_data.name:
            raise ValueError("Имя товара уже используется")
        else:
            raise ValueError("Товар не найден")


async def remove_product(session: AsyncSession, product_id: int):
    product = await get_product(session, product_id)
    if product:
        await del_product(session, product_id)
    else:
        raise ValueError("Продукт не найден")
