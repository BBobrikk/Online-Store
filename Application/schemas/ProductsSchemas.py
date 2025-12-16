from pydantic import BaseModel


class ProductsBase(BaseModel):
    name: str
    category: str


class ProductsCreate(ProductsBase):
    price: float


class ProductsRead(ProductsCreate):
    product_id: int


class ProductsUpdate(BaseModel):
    name: str | None = None
    category: str | None = None
    price: float | None = None
