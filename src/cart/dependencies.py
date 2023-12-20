from sqlalchemy.orm import joinedload

from sqlalchemy.orm.exc import NoResultFound

from sqlalchemy.exc import SQLAlchemyError
from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import CartItemPydantic

from db import get_async_session
from .models import *

from auth.auth import fastapi_users
from product.models import Product

from .exceptions import handle_exceptions


async def show_cart_items(current_user: User, session: AsyncSession):
    try:
        if current_user is None:
            raise HTTPException(status_code=404, detail="You are not authorized")
        cart_items = (
            await session.execute(
                select(CartItem).options(joinedload(CartItem.product))
                .where(CartItem.cart_id == current_user.cart.id)
            )).scalars().all()

    except SQLAlchemyError as e:
        await handle_exceptions(e)

    except Exception as e:
        await handle_exceptions(e)

    else:
        return cart_items


async def append_to_cart(product_id: int, current_user: User, session: AsyncSession):
    try:
        product = await session.execute(select(Product).where(Product.id == product_id))
        product = product.scalar_one_or_none()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Product not found")
    if not current_user.cart:
        cart = Cart(user=current_user)
        session.add(cart)
        await session.commit()
    cart_item = await session.execute(
        select(CartItem).where((CartItem.cart_id == current_user.cart.id) & (CartItem.product_id == product_id)))
    cart_item = cart_item.scalar_one_or_none()
    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = CartItem(cart=current_user.cart, product=product, quantity=1)
        session.add(cart_item)
    await session.commit()
    return {"message": "Product added to cart successfully"}


async def delete_item(item_id: int, session: AsyncSession):
    try:
        item = await session.get(CartItem, item_id)
        if item:
            await session.delete(item)
            await session.commit()
            return {"status": "success", "message": "Item removed from cart"}
        else:
            raise HTTPException(status_code=404, detail="Item not found in cart")
    except SQLAlchemyError as e:
        await handle_exceptions(e)
    except Exception as e:
        await handle_exceptions(e)
