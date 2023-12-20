from pydantic import BaseModel
from typing import Optional


class ProductCart(BaseModel):
    id: int
    name: str
    price: float

    class Config:
        orm_mode = True


class CartItemPydantic(BaseModel):
    id: int
    cart_id: int
    product: Optional[ProductCart]
    quantity: int

    class Config:
        orm_mode = True
