from Application.services.order_items_serv import (
    check_item,
    check_items,
    check_user_item,
    check_user_items,
    remove_order_item,
    add_order_item,
)
from Application.schemas import OrderItemsCreate, OrderItemsBase, OrderItemsRead
from fastapi import APIRouter, HTTPException, Depends
from Application.authorization.dependencies import require_auth, require_admin
from Application.utils.connecting_dep import SessionDep

order_item_router = APIRouter(prefix="/items", tags=["OrderItems"])


@order_item_router.get(
    "", response_model=list[OrderItemsBase], dependencies=[Depends(require_admin)]
)
async def check_items_api(session: SessionDep):
    try:
        return await check_items(session)
    except ValueError as er:
        raise HTTPException(detail=str(er), status_code=404)


@order_item_router.get("/me", response_model=list[OrderItemsBase])
async def check_user_items_api(
    session: SessionDep, order_id: int, user_id: int = Depends(require_auth)
):
    try:
        return await check_user_items(session, user_id, order_id)
    except ValueError as er:
        raise HTTPException(detail=str(er), status_code=404)


@order_item_router.delete("")
async def remove_item_api(
    session: SessionDep, order_id, item_id, user_id: int = Depends(require_auth)
):
    try:
        await remove_order_item(session, item_id, user_id, order_id)
        return {"status": "Товар удалён из заказа"}
    except ValueError as er:
        raise HTTPException(detail=str(er), status_code=404)


@order_item_router.post("")
async def create_item_api(
    session: SessionDep,
    item_data: OrderItemsCreate,
    user_id: int = Depends(require_auth),
):
    try:
        await add_order_item(session, user_id, item_data)
        return {"status": "Товар добавлен в заказ"}
    except ValueError as er:
        raise HTTPException(detail=str(er), status_code=404)


@order_item_router.get("/me/{item_id}", response_model=OrderItemsRead)
async def check_user_item_api(
    session: SessionDep,
    order_id: int,
    item_id: int,
    user_id: int = Depends(require_auth),
):
    try:
        return await check_user_item(session, user_id, order_id, item_id)
    except ValueError as er:
        raise HTTPException(detail=str(er), status_code=404)


@order_item_router.get(
    "/{item_id}", response_model=OrderItemsRead, dependencies=[Depends(require_admin)]
)
async def check_item_api(session: SessionDep, item_id: int):
    try:
        return await check_item(session, item_id)
    except ValueError as er:
        raise HTTPException(detail=str(er), status_code=404)
