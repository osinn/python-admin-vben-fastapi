import asyncio
import os
from contextlib import asynccontextmanager
from pathlib import Path

import redis
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from redis import AuthenticationError, RedisError

# 导入公共环境配置
from core.framework.cache_tools import cache

from core.framework.log_tools import logger
from core.framework.tools import import_modules_async
from core.framework.scheduler_tools import job_scheduler, scheduler_manager
from core.utils.ip_utils_ip2region import ip_location_service

from dotenv import load_dotenv

def load_environment():
    """加载环境变量"""
    # 从环境变量获取路径
    env_file = os.getenv("ENV_FILE")
    # 使用系统环境变量
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if env_file and Path(f"{base_dir}/config/{env_file}").exists():
        # 从指定路径加载
        load_dotenv(dotenv_path=f"{base_dir}/config/{env_file}")
        print(f"Loaded env from: {base_dir}/config/{env_file}")
        logger.info(f"Loaded env from: {base_dir}/config/{env_file}")
    else:
        load_dotenv(dotenv_path=f"{base_dir}/config/.env")
        environment = os.getenv("ENVIRONMENT", "dev")
        load_dotenv(dotenv_path=f"{base_dir}/config/.env.{environment}")
        print(f"Loaded env from: {base_dir}/config/.env.{environment}")
        logger.info(f"Loaded env from: {base_dir}/config/.env.{environment}")

# 加载环境变量
load_environment()

MYSQL_HOST = os.getenv("MYSQL_HOST", "127.0.0.1")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "123456")
MYSQL_DB = os.getenv("MYSQL_DB", "osinn_vben")

REDIS_HOST = os.getenv("REDIS_HOST", "127.0.0.1")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)

"""安全警告: 不要在生产中打开调试运行!"""

DEBUG = os.getenv("DEBUG", "True").lower() == "true"

logger.info(f"启动环境：{DEBUG}")

# ----------------------------------------------

"""
Mysql 数据库配置项
连接引擎官方文档：https://www.osgeo.cn/sqlalchemy/core/engines.html
数据库链接配置说明：mysql+asyncmy://数据库用户名:数据库密码@数据库地址:数据库端口/数据库名称
"""
# 数据库
SQLALCHEMY_DATABASE_URL = f"mysql+asyncmy://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
# 任务调度连接数据库地址
APSCHEDULER_DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}?charset=utf8"

"""
Redis 数据库配置
"""
REDIS_DB_ENABLE = True
REDIS_DB_CONFIG = {
    "host": REDIS_HOST,
    "port": REDIS_PORT,
    "password": REDIS_PASSWORD,
    "decode_responses": True,
    "db": 0
}

"""
是否开启定时任务调度
"""
APSCHEDULER_ENABLE = True


# ----------------------------------------------

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 360 # token 6 小时过期
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

"""
跨域解决
详细解释：https://cloud.tencent.com/developer/article/1886114
官方文档：https://fastapi.tiangolo.com/tutorial/cors/
"""
# 是否启用跨域
CORS_ORIGIN_ENABLE = True
# 只允许访问的域名列表，* 代表所有
ALLOW_ORIGINS = ["*"]
# 是否支持携带 cookie
ALLOW_CREDENTIALS = True
# 设置允许跨域的http方法，比如 get、post、put等。
ALLOW_METHODS = ["*"]
# 允许携带的headers，可以用来鉴别来源等作用。
ALLOW_HEADERS = ["*"]

EVENTS = [
    "config.settings.connect_redis" if REDIS_DB_ENABLE else None,
    "config.settings.run_apscheduler" if APSCHEDULER_ENABLE else None,
]

@asynccontextmanager # 装饰器将生成器函数转换为异步上下文管理器
async def lifespan(app: FastAPI):
    # 注册任务调度装饰器
    import apps.modules.sys.scheduler.job.registry

    # 应用程序启动时执行
    await import_modules_async(EVENTS, "全局事件", app=app, status=True)

    # --- startup ---
    async def run_init():
        from core.framework.database_config import session_factory
        async with session_factory() as db:
            await scheduler_manager.register_all_tasks(db)
    await run_init()
    # yield 之前：进入上下文时执行的代码（设置/初始化）
    # yield 之后：退出上下文时执行的代码（清理/关闭）
    yield
    # 应用程序关闭时执行
    await import_modules_async(EVENTS, "全局事件", app=app, status=False)
    ip_location_service.close()

# 连接redis
async def connect_redis(app: FastAPI, status: bool):
    """
    连接redis
    :param app:
    :param status:
    :return:
    """
    if status:
        logger.info("连接Redis")
        rd = redis.asyncio.Redis(**REDIS_DB_CONFIG) #aioredis.from_url(REDIS_DB_URL, decode_responses=True, health_check_interval=1, db=1)
        app.state.redis = rd
        try:
            response = await rd.ping()
            if response:
                print("Redis 连接成功")
                cache.init_redis(app.state.redis)
            else:
                print("Redis 连接失败")
        except AuthenticationError as e:
            raise AuthenticationError(f"Redis 连接认证失败，用户名或密码错误: {e}")
        except TimeoutError as e:
            raise TimeoutError(f"Redis 连接超时，地址或者端口错误: {e}")
        except RedisError as e:
            raise RedisError(f"Redis 连接失败: {e}")
    else:
        print("Redis 连接关闭")
        try:
            if app.state.redis:
                await app.state.redis.connection_pool.disconnect()
                await cache.get_redis_connect().close()
        except Exception as e:
            print("关闭Redis连接异常")
            logger.error(f"关闭Redis连接异常: {e}")

# 运行 apschedule 定时任务
async def run_apscheduler(app: FastAPI, status: bool):
    if status:
        print("启动apschedule任务调度")
        logger.info("启动apschedule任务调度")
        job_scheduler.init_scheduler(APSCHEDULER_DATABASE_URL)
    else:
        try:
            print("关闭apschedule任务调度")
            job_scheduler.shutdown()
        except Exception as e:
            print("关闭apschedule任务调度失败")
            logger.error(f"关闭apschedule任务调度失败: {e}")