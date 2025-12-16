from Application.schemas import (
    ProductsCreate,
    ProductsUpdate,
    ProductsRead,
    ProductsBase,
)
from Application.authorization.dependencies import require_admin
from fastapi import HTTPException, APIRouter, Depends
from Application.services.products_serv import (
    update_product_serv,
    check_product,
    check_products,
    remove_product,
    add_product,
)
from Application.utils.connecting_dep import SessionDep

product_router = APIRouter(prefix="/products", tags=["Products"])


@product_router.get("", response_model=list[ProductsBase])
async def get_products_api(session: SessionDep):
    try:
        return await check_products(session)
    except ValueError as er:
        raise HTTPException(detail=str(er), status_code=404)


@product_router.get("/{product_id}", response_model=ProductsRead)
async def get_products_api(session: SessionDep, product_id: int):
    try:
        return await check_product(session, product_id)
    except ValueError as er:
        raise HTTPException(detail=str(er), status_code=404)


@product_router.post("", dependencies=[Depends(require_admin)])
async def create_product_api(session: SessionDep, product_data: ProductsCreate):
    try:
        await add_product(session, product_data)
        return {"status": "Товар добавлен"}
    except ValueError as er:
        raise HTTPException(detail=str(er), status_code=409)


@product_router.put("/{product_id}", dependencies=[Depends(require_admin)])
async def update_product_api(
    session: SessionDep, product_data: ProductsUpdate, product_id: int
):
    try:
        await update_product_serv(session, product_data, product_id)
        return {"status": "Данные обновлены"}
    except ValueError as er:
        raise HTTPException(detail=str(er), status_code=409)


@product_router.delete("/{product_id}", dependencies=[Depends(require_admin)])
async def delete_product_api(session: SessionDep, product_id: int):
    try:
        await remove_product(session, product_id)
        return {"status": "Товар удалён"}
    except ValueError as er:
        raise HTTPException(detail=str(er), status_code=404)
