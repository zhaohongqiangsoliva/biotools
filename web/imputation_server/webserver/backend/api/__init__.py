"""
create app
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise

from .v1 import v1
from core import settings


app = FastAPI(title=settings.TITLE, description=settings.DESC)


app.include_router(v1, prefix="/imputation")

# async def do_stuff():
#     """关闭数据库"""
#     await Tortoise.close_connections()


# async def init():
#     """创建数据库"""
#     await Tortoise.init(
#         db_url=settings.db_url,
#         modules={'models': ['models']}
#     )
#     await Tortoise.generate_schemas()
# 可以不要
# @app.on_event("startup")
# async def startup():
#     """aioredis"""
#     app.state.redis: Redis = await aioredis.from_url("redis://127.0.0.1:6379",  decode_responses=True)
#
#
# @app.on_event("shutdown")
# async def shutdown():
#     """close redis"""
#     await app.state.redis.close()

# @app.on_event("startup")
# async def startup_event():
#     """添加在应用程序启动之前运行初始化数据库"""
#     await init()


# @app.on_event("shutdown")
# async def shutdown_event():
#     """添加在应用程序关闭时关闭所有数据库链接"""
#     await do_stuff()


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


register_tortoise(
    app,
    db_url="mysql://root:e8c87vb2@118.195.223.193:3306/imputationcomputed",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

