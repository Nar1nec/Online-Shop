from sqlalchemy.orm import joinedload

from sqlalchemy.exc import SQLAlchemyError
from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import CartItemPydantic
from .dependencies import *

from db import get_async_session
from .models import *

from auth.auth import fastapi_users
from product.models import Product

current_user = fastapi_users.current_user()

router = APIRouter(
    prefix="/cart",
    tags=["Cart"],
)


@router.get("/", response_model=list[CartItemPydantic])
async def get_cart_items(current_user: User = Depends(current_user),
                         session: AsyncSession = Depends(get_async_session)):
    return await show_cart_items(current_user, session)


@router.post("/add_to_cart/{product_id}")
async def add_to_cart(
        product_id: int,
        current_user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await append_to_cart(product_id, current_user, session)


@router.delete("/remove_from_cart/{item_id}")
async def remove_item_from_cart(item_id: int, session: AsyncSession = Depends(get_async_session)):
    return await delete_item(item_id, session)
