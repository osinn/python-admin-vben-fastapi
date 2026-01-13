"""
导入 SQLAlchemy 部分
安装： pip install sqlalchemy[asyncio]
官方文档：https://docs.sqlalchemy.org/en/20/intro.html#installation
"""
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from config.settings import SQLALCHEMY_DATABASE_URL, REDIS_DB_ENABLE
from fastapi import Request
from core.framework.exception import BizException

from core.utils.Snowflake import snowflake

# 官方文档：https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.create_async_engine

# database_url  dialect+driver://username:password@host:port/database

# echo：如果为True，引擎将记录所有语句以及它们的参数列表的repr()到默认的日志处理程序，该处理程序默认为sys.stdout。如果设置为字符串"debug"，
# 结果行也将打印到标准输出。Engine的echo属性可以随时修改以打开和关闭日志记录；也可以使用标准的Python logging模块来直接控制日志记录。

# echo_pool=False：如果为True，连接池将记录信息性输出，如何时使连接失效以及何时将连接回收到默认的日志处理程序，该处理程序默认为sys.stdout。
# 如果设置为字符串"debug"，记录将包括池的检出和检入。也可以使用标准的Python logging模块来直接控制日志记录。

# pool_pre_ping：布尔值，如果为True，将启用连接池的"pre-ping"功能，该功能在每次检出时测试连接的活动性。

# pool_recycle=-1：此设置导致池在给定的秒数后重新使用连接。默认为-1，即没有超时。例如，将其设置为3600意味着在一小时后重新使用连接。
# 请注意，特别是MySQL会在检测到连接8小时内没有活动时自动断开连接（尽管可以通过MySQLDB连接自身和服务器配置进行配置）。

# pool_size=5：在连接池内保持打开的连接数。与QueuePool以及SingletonThreadPool一起使用。
# 对于QueuePool，pool_size设置为0表示没有限制；要禁用连接池，请将poolclass设置为NullPool。

# pool_timeout=30：在从池中获取连接之前等待的秒数。仅在QueuePool中使用。这可以是一个浮点数，但受Python时间函数的限制，可能在几十毫秒内不可靠

# max_overflow 参数用于配置连接池中允许的连接 "溢出" 数量。这个参数用于在高负载情况下处理连接请求的峰值。
# 当连接池的所有连接都在使用中时，如果有新的连接请求到达，连接池可以创建额外的连接来满足这些请求，最多创建的数量由 max_overflow 参数决定。

# 创建数据库连接
async_engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo="debug" # 打印执行SQL以及结果
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
