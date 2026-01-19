import asyncio
import traceback
from functools import wraps

from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from core.framework.crud_async_session import AsyncGenericCRUD
from core.framework.exception import BizException


def transaction(func):
    """
    事务装饰器
    :param func:
    :return:
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        db = None
        for arg in kwargs.items():
            if isinstance(arg, Session):
                db = arg
                break
            if isinstance(arg, AsyncSession):
                db = arg
                break
            if isinstance(arg, AsyncGenericCRUD):
                db = arg.db
                break
        if not db:
            for kw in kwargs.values():
                if isinstance(kw, Session):
                    db = kw
                    break
                if isinstance(kw, AsyncSession):
                    db = kw
                    break
                if isinstance(kw, AsyncGenericCRUD):
                    db = kw.db
                    break
        if not db:
            raise BizException(msg="服务异常，请联系管理员", error="未找到数据库会话")

        try:
            result = await func(*args, **kwargs) if asyncio.iscoroutinefunction(func) else func(*args, **kwargs)
            await db.commit() if asyncio.iscoroutinefunction(func) else db.commit()
            return result
        # except OperationalError as e:
        #     # 异常时回滚事务
        #     await db.rollback() if asyncio.iscoroutinefunction(func) else db.rollback()
        #     print(f"事务提交失败：{traceback.format_exc()}")
        #     raise BizException(msg="服务异常，请联系管理员", error=str(e))
        except Exception as e:
            await db.rollback() if asyncio.iscoroutinefunction(func) else db.rollback()
            raise BizException(msg="服务异常，请联系管理员", error=str(e))

    return wrapper