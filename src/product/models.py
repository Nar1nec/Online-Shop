from sqlalchemy import Column, Integer, String, Float, CheckConstraint, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from auth.models import User

from db import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    products = relationship("Product", back_populates="category", lazy='selectin')


class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    description = Column(String)
    image_path = Column(String)
    category_id = Column(Integer, ForeignKey("categories.id"))

    __table_args__ = (
        CheckConstraint('price >= 0', name='check_price_non_negative'),
    )

    category = relationship("Category", back_populates="products")
    cart_items = relationship("CartItem", back_populates="product", lazy='selectin')

