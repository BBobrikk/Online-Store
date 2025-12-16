from fastapi import APIRouter, HTTPException, Depends
from Application.authorization.dependencies import require_auth, require_admin
from Application.schemas import UsersUpdate, UsersRead, BaseUser
from Application.utils.connecting_dep import SessionDep
from Application.services.users_serv import (
    check_users,
    check_user,
    update_user_info,
    remove_user,
)

user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.get(
    "", response_model=list[BaseUser], dependencies=[Depends(require_admin)]
)
async def get_users_api(session: SessionDep):
    try:
        return await check_users(session)
    except ValueError as er:
        raise HTTPException(detail=str(er), status_code=404)


@user_router.get("/me", response_model=UsersRead)
async def get_profile_api(session: SessionDep, user_id: int = Depends(require_auth)):
    try:
        return await check_user(session, user_id)
    except ValueError as er:
        raise HTTPException(detail=str(er), status_code=404)


@user_router.put("/me")
async def update_user_api(
    session: SessionDep, user_data: UsersUpdate, user_id: int = Depends(require_auth)
):
    try:
        await update_user_info(session, user_data, user_id)
        return {"status": "Данные обновлены"}
    except ValueError as er:
        raise HTTPException(detail=str(er), status_code=404)


@user_router.delete("/me")
async def delete_user_api(session: SessionDep, user_id: int = Depends(require_auth)):
    try:
        await remove_user(session, user_id)
        return {"status": "Пользователь успешно удалён"}
    except ValueError as er:
        raise HTTPException(detail=str(er), status_code=404)
