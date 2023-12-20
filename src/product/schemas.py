from typing import Optional

from pydantic import BaseModel



class ProductBase(BaseModel):
    id: int
    name: str
    price: float
    description: str
    image_path: str


class ProductAdmin(BaseModel):
    id: int
    name: str
    price: float


class ProductCreate(BaseModel):
    name: str
    price: float
    description: str
    image_path: str
    category_id: int


class ProductResponse(ProductBase):
    class Config:
        orm_mode = True
