from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse
from bcrypt import gensalt, hashpw, checkpw
from Application.schemas import UsersCreds
from Application.authorization.config import security
from Application.repositories.users_rep import get_user_by_email


async def registration(user_id: int, role: str):
    token = security.create_access_token(uid=str(user_id), data={"role": role})

    response = JSONResponse({"status": "Успешная регистрация", "token": token})

    return response


async def hash_password(password: str):
    password_hash = hashpw(password.encode(), gensalt())
    return password_hash.decode()


async def login(session: AsyncSession, credentials: UsersCreds):
    user = await get_user_by_email(session, credentials.email)
    if user:
        if checkpw(credentials.password.encode(), user.password_hash.encode()):
            token = security.create_access_token(
                uid=str(user.user_id), data={"role": user.role}
            )

            response = JSONResponse({"status": "Успешная регистрация", "token": token})

            return response
        raise HTTPException(detail="Пароль неверен", status_code=401)
    raise HTTPException(detail="Электронная почта не найдена", status_code=404)


# async def logout():
#     response = JSONResponse({"status" : "Выход из системы"})
#     security.unset(response)
#     return response
