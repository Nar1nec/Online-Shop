from sqlalchemy import Column, Integer,ForeignKey
from sqlalchemy.orm import relationship

from auth.models import User

from db import Base


class Cart(Base):
    __tablename__ = "carts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False, unique=True)

    # Добавляем связь с пользователем и корзинными элементами
    user = relationship("User", back_populates="cart", lazy='selectin')
    items = relationship("CartItem", back_populates="cart", primaryjoin="Cart.id == CartItem.cart_id", lazy='selectin')


class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey("carts.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("product.id"))
    quantity = Column(Integer, default=1)

    cart = relationship("Cart", back_populates="items", lazy='selectin')
    product = relationship("Product", back_populates="cart_items", lazy='selectin')