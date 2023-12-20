from sqlalchemy.exc import SQLAlchemyError
from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from .dependencies import *

from .schemas import ProductResponse

from db import get_async_session
from .models import *

from auth.auth import fastapi_users

current_user = fastapi_users.current_user()

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.get("/{category_name}", response_model=list[ProductResponse])
async def get_category_name_product(category_name: str, session: AsyncSession = Depends(get_async_session)):
    return await get_product(category_name, session)
