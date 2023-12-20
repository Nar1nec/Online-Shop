import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth.auth import auth_backend, fastapi_users

from auth.schemas import UserRead, UserCreate

from product.router import router as router_product
from pages.router import router as router_pages
from cart.router import router as router_cart
from admin.router import router as router_admin

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi.staticfiles import StaticFiles

from redis import asyncio as aioredis

app = FastAPI()

app.mount("/static", StaticFiles(directory="src/static"), name="static")

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET","POST","DELETE"],
    allow_headers=["*"],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(router_product)
app.include_router(router_pages)
app.include_router(router_cart)
app.include_router(router_admin)


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)