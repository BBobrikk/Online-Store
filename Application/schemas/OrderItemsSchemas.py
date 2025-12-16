from pydantic import BaseModel


class OrderItemsBase(BaseModel):
    order_id: int
    product_id: int

    class Config:
        from_attributes = True


class OrderItemsCreate(OrderItemsBase):
    quantity: int

    class Config:
        from_attributes = True


class OrderItemsRead(OrderItemsCreate):
    order_item_id: int
