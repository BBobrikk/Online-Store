from Application.services.orders_serv import (
    check_order,
    check_user_order,
    check_user_orders,
    check_orders,
    change_status,
    add_order,
)
from Application.schemas import OrdersRead
from fastapi import APIRouter, HTTPException, Depends
from Application.authorization.dependencies import require_auth, require_admin
from Application.utils.connecting_dep import SessionDep

order_router = APIRouter(prefix="/orders", tags=["Orders"])


@order_router.get(
    "", dependencies=[Depends(require_admin)], response_model=list[OrdersRead]
)
async def check_orders_api(session: SessionDep):
    try:
        return await check_orders(session)
    except ValueError as er:
        raise HTTPException(detail=str(er), status_code=404)


@order_router.get("/me", response_model=list[OrdersRead])
async def check_user_orders_api(
    session: SessionDep, user_id: int = Depends(require_auth)
):
    try:
        return await check_user_orders(session, user_id)
    except ValueError as er:
        raise HTTPException(detail=str(er), status_code=404)


@order_router.post("")
async def create_order_api(session: SessionDep, user_id: int = Depends(require_auth)):
    await add_order(session, user_id)
    return {"status": "Заказ успешно создан"}


@order_router.get(
    "/{order_id}", dependencies=[Depends(require_admin)], response_model=OrdersRead
)
async def check_order_api(session: SessionDep, order_id: int):
    try:
        return await check_order(session, order_id)
    except ValueError as er:
        raise HTTPException(detail=str(er), status_code=404)


@order_router.get("/me/{order_id}", response_model=OrdersRead)
async def check_user_order_api(
    session: SessionDep, order_id: int, user_id: int = Depends(require_auth)
):
    try:
        return await check_user_order(session, user_id, order_id)
    except ValueError as er:
        raise HTTPException(detail=str(er), status_code=404)


@order_router.put("")
async def update_status_api(session: SessionDep, order_id: int, user_id : int = Depends(require_auth)):
    try:
        await change_status(session, order_id)
        return {"status": "Статус заказа изменён"}
    except ValueError as er:
        raise HTTPException(detail=str(er), status_code=404)
