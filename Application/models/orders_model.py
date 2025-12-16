from Application.core.connection import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey, CheckConstraint


class OrdersORM(Base):

    __tablename__ = "Orders"

    order_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("Users.user_id"))
    status: Mapped[str]
    user: Mapped["UsersORM"] = relationship(back_populates="orders")
    order_items: Mapped[list["OrderItemsORM"]] = relationship(back_populates="order")

    __table_args__ = (
        CheckConstraint("status in ('on the way','delivered', 'received')"),
    )
