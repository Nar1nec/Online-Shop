from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from fastapi_cache.decorator import cache
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from .models import *

from auth.auth import fastapi_users
from .schemas import ProductCreate

current_user = fastapi_users.current_user()


async def delete_product(product_id: int, session: AsyncSession):
    try:
        product = await session.get(Product, product_id)
        if product:
            await session.delete(product)
            await session.commit()
        else:
            raise HTTPException(status_code=404, detail="Product not found")
    except SQLAlchemyError as e:
        print(f"SQLAlchemyError: {e}")
        raise HTTPException(status_code=500, detail={"status": "error", "data": None, "details": str(e)})
    except Exception as e:
        print(f"Unexpected Error: {e}")
        raise HTTPException(status_code=500, detail={"status": "error", "data": None, "details": str(e)
        })
    else:
        return {"status": "success", "message": "Product removed"}


async def set_product(new_product: ProductCreate, session: AsyncSession):
    try:
        stmt = insert(Product).values(**new_product.dict())
        await session.execute(stmt)
        await session.commit()
    except SQLAlchemyError as e:
        print(f"SQLAlchemyError: {e}")
        raise HTTPException(status_code=500, detail={"status": "error", "data": None, "details": str(e)})
    except Exception as e:
        print(f"Unexpected Error: {e}")
        raise HTTPException(status_code=500, detail={"status": "error", "data": None, "details": str(e)})
    return {"status": "success"}


async def get_product(category_name: str, session: AsyncSession):
    try:
        category = await session.execute(select(Category).where(Category.name == category_name))
        category = category.scalar_one_or_none()

        if category is None:
            raise HTTPException(status_code=404, detail="Category not found")

        query = select(Product).where(Product.category_id == category.id)
        products = await session.execute(query)

    except SQLAlchemyError as e:
        print(f"SQLAlchemyError: {e}")
        raise HTTPException(status_code=500, detail={"status": "error", "data": None, "details": str(e)})
    except Exception as e:
        print(f"Unexpected Error: {e}")
        raise HTTPException(status_code=500, detail={"status": "error", "data": None, "details": str(e)})
    else:
        return products.scalars().all()


async def set_category(category_name: str, session: AsyncSession):
    try:
        stmt = insert(Category).values({"name": category_name})
        await session.execute(stmt)
        await session.commit()
    except SQLAlchemyError as e:
        print(f"SQLAlchemyError: {e}")
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": str(e)
        })
    except Exception as e:
        print(f"Unexpected Error: {e}")
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": str(e)
        })
    else:
        return {"status": "success"}
