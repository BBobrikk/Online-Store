from pydantic import BaseModel


class OrdersCreate(BaseModel):
    user_id: int
    status: str


class OrdersRead(OrdersCreate):
    order_id: int
