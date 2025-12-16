from sqlalchemy import CheckConstraint

from Application.core.connection import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship


class UsersORM(Base):

    __tablename__ = "Users"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    firstname: Mapped[str]
    lastname: Mapped[str]
    email: Mapped[str]
    password_hash: Mapped[str]
    role: Mapped[str]
    is_active: Mapped[bool]
    orders: Mapped[list["OrdersORM"]] = relationship(back_populates="user")

    __table_args__ = (CheckConstraint("role in ('user','admin')"),)
