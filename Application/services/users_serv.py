from Application.authorization.routers import registration, hash_password
from Application.schemas import UsersUpdate, UsersCreate
from sqlalchemy.ext.asyncio import AsyncSession
from Application.repositories.users_rep import (
    get_user,
    get_users,
    del_user,
    update_user,
    create_user,
    get_user_by_email,
)


async def check_users(session: AsyncSession):
    users = await get_users(session)
    if users:
        return users
    raise ValueError("Пользователи не найдены")


async def check_user(session: AsyncSession, user_id: int):
    user = await get_user(session, user_id)
    if user and user.is_active:
        return user
    raise ValueError("Пользователь не найден")


async def add_user(session: AsyncSession, user_data: UsersCreate):
    email = user_data.email
    user = await get_user_by_email(session, email)
    if user and user.is_active is True:
        raise ValueError("Электронная почта зарегистрирована")

    if user_data.password != user_data.repeat_pass:
        raise ValueError("Пароли не совпадают")

    if user_data.email == "admin@gmail.com":
        role = "admin"
    else:
        role = "user"

    password_hash = await hash_password(user_data.password)

    await create_user(session, user_data, password_hash, role)

    user = await get_user_by_email(session, user_data.email)

    return await registration(user.user_id, role)


async def update_user_info(session: AsyncSession, user_data: UsersUpdate, user_id: int):
    users = await get_users(session)
    for user in users:
        if user.email == user_data.email and user.user_id == user_id:
            await update_user(session, user_data, user_id)
            print("CCCC")
        elif user.email != user_data.email and user.user_id == user_id:
            print("BBB")
            await update_user(session, user_data, user_id)
        elif user.email == user_data.email and user.user_id != user_id:
            print(user.user_id)
            raise ValueError("Электронная почта занята")


async def remove_user(session: AsyncSession, user_id: int):
    user = await get_user(session, user_id)
    if user and user.is_active is True:
        await del_user(session, user_id)
    else:
        raise ValueError("Пользователь не найден")
