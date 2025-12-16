from sqlalchemy import select
from Application.models import UsersORM
from Application.schemas import UsersCreate, UsersUpdate
from sqlalchemy.ext.asyncio import AsyncSession


async def get_users(session: AsyncSession):
    query = select(UsersORM)
    result = await session.execute(query)
    return result.scalars().all()


async def get_user(session: AsyncSession, user_id: int):
    user = await session.get(UsersORM, user_id)
    return user


async def get_user_by_email(session: AsyncSession, email: str):
    query = select(UsersORM).where(UsersORM.email == email)
    result = await session.execute(query)
    return result.scalars().first()


async def create_user(
    session: AsyncSession, user_data: UsersCreate, pass_hash: str, role: str
):
    user = UsersORM(
        email=user_data.email,
        firstname=user_data.firstname,
        lastname=user_data.lastname,
        password_hash=pass_hash,
        role=role,
        is_active=True,
    )

    session.add(user)


async def update_user(session: AsyncSession, user_data: UsersUpdate, user_id):
    user = await get_user(session, user_id)
    items = user_data.model_dump(exclude_unset=True).items()
    for item, value in items:
        setattr(user, item, value)


async def del_user(session: AsyncSession, user_id):
    user = await get_user(session, user_id)
    user.is_active = False
