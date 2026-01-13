"""
导入 SQLAlchemy 部分
安装： pip install sqlalchemy[asyncio]
官方文档：https://docs.sqlalchemy.org/en/20/intro.html#installation
"""
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import  AsyncSession, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column
from sqlalchemy import DateTime, BIGINT, func, Boolean, inspect
from datetime import datetime

from core.utils.Snowflake import snowflake

class Base(AsyncAttrs, DeclarativeBase):
    """
    创建基本映射类
    稍后，我们将继承该类，创建每个 ORM 模型
    """

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """
        将表名改为小写
        如果有自定义表名就取自定义，没有就取小写类名
        """
        table_name = cls.__tablename__
        if not table_name:
            model_name = cls.__name__
            ls = []
            for index, char in enumerate(model_name):
                if char.isupper() and index != 0:
                    ls.append("_")
                ls.append(char)
            table_name = "".join(ls).lower()
        return table_name


class BaseEntity(Base):
    """
    公共 ORM 模型，基表
    """
    __abstract__ = True

    id:  Mapped[int] = mapped_column(BIGINT, primary_key=True, comment='主键ID',
                                     default=lambda: str(snowflake.generate_id()),
                                     server_default=str(snowflake.generate_id())
                                     )

    created_time: Mapped[datetime] = mapped_column(DateTime,
                                                   default=func.now(), # 新增时添加默认值
                                                   server_default=func.now(), comment='创建时间')
    created_by: Mapped[int] = mapped_column(BIGINT, comment='创建人ID')
    updated_time: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        comment='更新时间'
    )
    updated_by: Mapped[int] = mapped_column(BIGINT, comment='更新人ID')
    # bool 对应MySQL类型tinyint(1)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false", comment="是否软删除")

    @classmethod
    def get_column_attrs(cls) -> list:
        """
        获取模型中除 relationships 外的所有字段名称
        :return:
        """
        mapper = inspect(cls)

        return mapper.column_attrs.keys()

    @classmethod
    def get_attrs(cls) -> list:
        """
        获取模型所有字段名称
        :return:
        """
        mapper = inspect(cls)
        return mapper.attrs.keys()

    @classmethod
    def get_relationships_attrs(cls) -> list:
        """
        获取模型中 relationships 所有字段名称
        :return:
        """
        mapper = inspect(cls)
        return mapper.relationships.keys()


async def db_getter() -> AsyncGenerator[AsyncSession, None]:
    from core.framework.database_config import session_factory
    """
    获取主数据库会话

    数据库依赖项，它将在单个请求中使用，然后在请求完成后将其关闭。更改model值会在请求结束时自动保存到数据库中

    函数的返回类型被注解为 AsyncGenerator[int, None]，其中 AsyncSession 是生成的值的类型，而 None 表示异步生成器没有终止条件。
    """
    async with session_factory() as session:
        # 创建一个新的事务，半自动 commit
        async with session.begin():
            yield session
