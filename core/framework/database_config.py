"""
导入 SQLAlchemy 部分
安装： pip install sqlalchemy[asyncio]
官方文档：https://docs.sqlalchemy.org/en/20/intro.html#installation
"""
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from config.settings import SQLALCHEMY_DATABASE_URL, REDIS_DB_ENABLE, DEBUG
from fastapi import Request
from core.framework.exception import BizException

# 官方文档：https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.create_async_engine

# 创建数据库连接
async_engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=DEBUG # 打印执行SQL以及结果
)

# 创建数据库会话
session_factory = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    expire_on_commit=False,
    class_=AsyncSession
)

# 数据库配置结束==========================

def redis_getter(request: Request) -> Redis:
    """
    获取 redis 数据库对象

    全局挂载，使用一个数据库对象
    """
    if not REDIS_DB_ENABLE:
        raise BizException("请先配置Redis数据库链接并启用！", desc="请启用 application/settings.py: REDIS_DB_ENABLE")
    return request.app.state.redis

#
#
# def mongo_getter(request: Request) -> AsyncIOMotorDatabase:
#     """
#     获取 mongo 数据库对象
#
#     全局挂载，使用一个数据库对象
#     """
#     if not MONGO_DB_ENABLE:
#         raise BizException(
#             msg="请先开启 MongoDB 数据库连接！",
#             desc="请启用 application/settings.py: MONGO_DB_ENABLE"
#         )
#     return request.app.state.mongo
