from Application.api.auth_api import auth_router
from Application.api.order_items_api import order_item_router
from Application.api.orders_api import order_router
from Application.api.products_api import product_router
from Application.utils.setup_database import setup_db
from uvicorn import run
from contextlib import asynccontextmanager
from fastapi import FastAPI
from Application.api.users_api import user_router


@asynccontextmanager
async def lifespan(app: FastAPI):

    await setup_db()

    yield


app = FastAPI(lifespan=lifespan)

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(product_router)
app.include_router(order_router)
app.include_router(order_item_router)

if __name__ == "__main__":
    run("main:app", reload=True)
