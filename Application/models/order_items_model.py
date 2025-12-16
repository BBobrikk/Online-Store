from Application.core.connection import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey


class OrderItemsORM(Base):

    __tablename__ = "Order_Items"

    order_item_id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("Orders.order_id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("Products.product_id"))
    quantity: Mapped[int]
    order: Mapped["OrdersORM"] = relationship(back_populates="order_items")
