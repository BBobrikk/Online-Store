from Application.core.connection import Base
from sqlalchemy.orm import mapped_column, Mapped


class ProductsORM(Base):

    __tablename__ = "Products"

    product_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    category: Mapped[str]
    price: Mapped[float]
