from fastapi import APIRouter, HTTPException
from Application.authorization.routers import login
from Application.schemas import UsersCreate, UsersCreds
from Application.utils.connecting_dep import SessionDep
from Application.services.users_serv import add_user

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/register")
async def registration_user(session: SessionDep, user_data: UsersCreate):
    try:
        return await add_user(session, user_data)
    except ValueError as er:
        raise HTTPException(detail=str(er), status_code=409)


@auth_router.post("/login")
async def login_user(session: SessionDep, creds: UsersCreds):
    try:
        return await login(session, creds)
    except ValueError as er:
        raise HTTPException(detail=str(er), status_code=404)


# @auth_router.post("/logout")
# async def logout_user():
#     return await logout()
