from typing import List, Optional, Annotated

from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.security import HTTPBasicCredentials
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from admin.router import search_products
from auth.models import User
from cart.router import get_cart_items
from db import get_async_session
from product.router import get_product

from cart.schemas import CartItemPydantic

from auth.auth import fastapi_users
from product.schemas import ProductAdmin

current_user = fastapi_users.current_user()

router = APIRouter(
    prefix="/pages",
    tags=["Pages"]
)

templates = Jinja2Templates(directory="src/templates")


@router.get("/auth")
def get_auth_page(request: Request):
    return templates.TemplateResponse("/auth/auth.html", {"request": request})


@router.get("/base")
def get_base_page(request: Request):
    return templates.TemplateResponse("/product/base.html", {"request": request})


@router.get("/cart")
def get_cart_page(request: Request, cart_items: List[CartItemPydantic] = Depends(get_cart_items)):
    return templates.TemplateResponse("/cart/cart.html", {"request": request, "cart_items": cart_items})


@router.get("/product/{category_name}")
async def get_product_page(request: Request, category_name: str, session: AsyncSession = Depends(get_async_session)):
    products = await get_product(category_name, session)
    return templates.TemplateResponse("/product/product.html", {"request": request, "products": products})


@router.get("/admin")
def get_admin_page(request: Request, user: User = Depends(current_user)):
    if user.email == "admin@mail.ru":
        return templates.TemplateResponse("/admin/admin.html", {"request": request})
    else:
        raise HTTPException(status_code=403, detail="Forbidden")


@router.get("/admin/categories")
def get_admin_page_products(request: Request, user: User = Depends(current_user)):
    if user.email == "admin@mail.ru":
        return templates.TemplateResponse("/admin/admin_categories.html", {"request": request})
    else:
        raise HTTPException(status_code=403, detail="Forbidden")


@router.get("/admin/products")
def get_admin_page_categories(request: Request,
                              user: User = Depends(current_user),
                              ):
    if user.email == "admin@mail.ru":
        return templates.TemplateResponse("/admin/admin_products.html", {"request": request, "products": []})
    else:
        raise HTTPException(status_code=403, detail="Forbidden")
