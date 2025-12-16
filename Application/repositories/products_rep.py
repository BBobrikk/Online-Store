from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from Application.schemas import ProductsCreate, ProductsUpdate
from Application.models import ProductsORM


async def get_products(session: AsyncSession):
    query = select(ProductsORM)
    result = await session.execute(query)
    return result.scalars().all()


async def get_product(session: AsyncSession, product_id: int):
    product = await session.get(ProductsORM, product_id)
    return product


async def get_product_by_name(session: AsyncSession, product_name: str):
    query = select(ProductsORM).where(ProductsORM.name == product_name)
    result = await session.execute(query)
    return result.scalars().all()


async def create_product(session: AsyncSession, product_data: ProductsCreate):
    product = ProductsORM(
        name=product_data.name, category=product_data.category, price=product_data.price
    )
    session.add(product)


async def update_product(
    session: AsyncSession, product_data: ProductsUpdate, product_id: int
):
    product = await get_product(session, product_id)
    items = product_data.model_dump(exclude_unset=True).items()
    for item, value in items:
        setattr(product, item, value)


async def del_product(session: AsyncSession, product_id: int):
    product = await get_product(session, product_id)
    await session.delete(product)
