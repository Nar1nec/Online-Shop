from typing import List, Annotated, Optional

from sqlalchemy.exc import SQLAlchemyError
from fastapi import APIRouter, Depends, HTTPException, Query, Form
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from product.dependencies import set_product, set_category, delete_product

from product.schemas import ProductAdmin, ProductCreate
from fastapi.templating import Jinja2Templates
from db import get_async_session
from fastapi import Request
from auth.auth import fastapi_users
from product.models import Product

current_user = fastapi_users.current_user()

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)

templates = Jinja2Templates(directory="src/templates")


@router.delete("/products/remove_product/{product_id}")
async def admin_remove_product(product_id: int, session: AsyncSession = Depends(get_async_session)):
    return await delete_product(product_id, session)


@router.post("/categories/add_category")
async def admin_add_category(name_category: Optional[Annotated[str, Form()]] = None, session: AsyncSession = Depends(get_async_session)):
    return await set_category(name_category, session)


@router.post("/products/add_products")
async def admin_add_product(new_product: ProductCreate, session: AsyncSession = Depends(get_async_session)):
    return await set_product(new_product, session)


@router.get("/products/get_products", response_model=List[ProductAdmin])
async def search_products(request: Request, name_product: Optional[Annotated[str, Form()]] = None,
                          session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(Product).where(Product.name.ilike(f"%{name_product}"))
        result = await session.execute(query)
        products = result.scalars().all()

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": str(e)
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": str(e)
        })
    else:
        print(products)
        return templates.TemplateResponse("/admin/admin_products.html", {"request": request, "products": products})
