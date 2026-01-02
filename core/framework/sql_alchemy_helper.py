from core.framework.logger import logger
from typing import Any, Dict, List, Optional, TypeVar, Type

from sqlalchemy import text, select, and_, func
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

from core.framework.common_schemas import PageVo
from core.framework.exception import BizException

T = TypeVar('T', bound=DeclarativeBase)

class SQLAlchemyHelper:

    """
    SQLAlchemy 助手
    # 执行查询并获取字典
    users_dict = helper.execute_to_dict(
        session,
        "SELECT * FROM users WHERE age > :age",
        {"age": 18}
    )

    result = await helper.execute_to_dicts(db, "SELECT * FROM tbl_user WHERE id = :id", {"id": 5})

    # 执行查询并获取模型对象
    stmt = text("SELECT * FROM products WHERE category = :category")
    result = session.execute(stmt, {"category": "electronics"})
    products = helper.result_to_model(result, Product)
    """
    @staticmethod
    def result_to_dict(result: Result) -> List[Dict[str, Any]]:
        """将查询结果转换为字典列表 - 使用 mappings()"""
        # 使用 result.mappings() 获取 RowMapping 对象
        return [dict(row) for row in result.mappings()]

    @staticmethod
    def first_to_dict(result: Result) -> Optional[Dict[str, Any]]:
        """将第一行结果转换为字典 - 使用 mappings()"""
        # 使用 mappings().first() 获取第一行
        row = result.mappings().first()
        return dict(row) if row else None

    @staticmethod
    def result_to_model(result: Result, model_class: Type[T]) -> List[T]:
        """将查询结果转换为模型对象列表 - 使用 mappings()"""
        # 使用 mappings() 获取 RowMapping
        rows = result.mappings().all()
        return [
            model_class(**dict(row))
            for row in rows
        ]

    @staticmethod
    def first_to_model(result: Result, model_class: Type[T]) -> Optional[T]:
        """将第一行结果转换为模型对象 - 使用 mappings()"""
        row = result.mappings().first()
        return model_class(**dict(row)) if row else None

    @staticmethod
    async def execute_scalars(
            session: AsyncSession,
            sql: str,
            params: dict = None
    ) -> List[Any]:
        """执行SQL查询返回标量值列表（第一列所有行）"""
        result: Result = await session.execute(text(sql), params or {})
        # 只会返回ID集合
        return list(result.scalars())

    @staticmethod
    async def execute_to_dicts(
            session: AsyncSession,
            sql: str,
            params: dict = None,
            chunk_size: int = None
    ) -> List[Dict[str, Any]]:
        """执行SQL查询返回字典列表，支持分块"""
        result: Result = await session.execute(text(sql), params or {})

        if chunk_size:
            # 分块处理大量数据
            all_data = []
            while True:
                rows = result.mappings().fetchmany(chunk_size)
                if not rows:
                    break
                all_data.extend([dict(row) for row in rows])
            return all_data
        else:
            return [dict(row) for row in result.mappings()]

    @staticmethod
    async def execute_first_model(
            session: AsyncSession,
            model_class: Type[T],
            sql: str,
            params: dict = None
    ) -> Optional[T]:
        """
        执行SQL查询返回第一个模型对象
        :param session: 数据库会话
        :param model_class: 转换映射模型
        :param sql: 执行SQL
        :param params: 查询参数
        :return:
        """
        result = await session.execute(text(sql), params or {})
        row = result.mappings().first()
        return model_class(**row) if row else None

    @staticmethod
    async def execute_model(
            session: AsyncSession,
            model_class: Type[T],
            sql: str,
            params: dict = None
    ) -> Optional[T]:
        """
        执行SQL查询返回一个集合模型对象
        :param session: 数据库会话
        :param model_class: 转换映射模型
        :param sql: 执行SQL
        :param params: 查询参数
        :return:
        """
        result = await session.execute(text(sql), params or {})
        rows = result.mappings().all()
        return [
            model_class(**dict(row))
            for row in rows
        ]


    @staticmethod
    async def select_records(
            session: AsyncSession,
            model_class: Type[T],
            filters: Optional[Dict[str, Any]] = None,
            order_by: Optional[List] = None,
            v_schema: Any = None
    ) -> List[T]:
        """
        通用 select 查询封装

        :param session: SQLAlchemy session
        :param model_class: 要查询的模型类，如 User
        :param filters: 过滤条件，字典形式，如 {"name": "Alice", "age": 30}
        :param order_by: 排序字段列表，如 [User.created_at.desc()]
        :param v_schema: 指定使用的序列化对象
        :return: 查询结果列表（模型对象列表）
        """
        stmt = select(model_class)

        # 添加过滤条件
        filter_conditions = []
        if filters:
            for key, value in filters.items():
                if not hasattr(model_class, key):
                    logger.info(f"Model {model_class.__name__} has no attribute '{key}'")
                    raise BizException("数据查询异常")
                column = getattr(model_class, key)
                filter_conditions.append(column == value)
            stmt = stmt.where(and_(*filter_conditions))
        # 添加排序
        if order_by:
            stmt = stmt.order_by(*order_by)

        result = await session.execute(stmt)
        rows = result.scalars().all()
        if rows and v_schema:
            return [v_schema.model_validate(obj) for obj in rows]
        else:
            return rows

    @staticmethod
    async def page_select_records(
            session: AsyncSession,
            model_class: Type[T],
            filters: Optional[Dict[str, Any]] = None,
            order_by: Optional[List] = None,
            limit: int = 10,
            offset: int = 1,
            v_schema: Any = None
    ) -> PageVo:
        """
        通用 分页 select 查询封装

        :param session: SQLAlchemy session
        :param model_class: 要查询的模型类，如 User
        :param filters: 过滤条件，字典形式，如 {"name": "Alice", "age": 30}
        :param order_by: 排序字段列表，如 [User.created_at.desc()]
        :param limit: 限制返回数量
        :param offset: 跳过记录数（用于分页）
        :param v_schema: 指定使用的序列化对象
        :return: 查询结果列表（模型对象列表）
        """
        stmt = select(model_class)

        # 添加过滤条件
        filter_conditions = []
        if filters:
            for key, value in filters.items():
                if not hasattr(model_class, key):
                    logger.info(f"Model {model_class.__name__} has no attribute '{key}'")
                    raise BizException("数据查询异常")
                column = getattr(model_class, key)
                filter_conditions.append(column == value)
            stmt = stmt.where(and_(*filter_conditions))

        # 查询总记录数
        count_stmt = select(func.count()).select_from(model_class)
        if filter_conditions:
            count_stmt = count_stmt.where(and_(*filter_conditions))
        count_result = await session.execute(count_stmt)
        total = count_result.scalar_one()

        # 添加排序
        if order_by:
            stmt = stmt.order_by(*order_by)

        if offset < 1:
            offset = 1
        if offset < 1:
            limit = 10

        offset = (offset - 1) * limit
        stmt.offset(offset).limit(limit)

        result = await session.execute(stmt)
        rows = result.scalars().all()
        if rows and v_schema:
            return PageVo(total, [v_schema.model_validate(obj).model_dump() for obj in rows])
        else:
            return PageVo(total, rows)


"""
示例
 参数1 数据库会话
 参数2 查询数据需要转换的模型
 参数3 需要执行的参数
 参数4 可选参数，查询参数
 users = await SQLAlchemyHelper.execute_model(db_session, UserEntity, "SELECT * FROM tbl_user")
 # 指定查询条件 ID等于5的用户
 users = await SQLAlchemyHelper.execute_model(db_session, UserEntity, "SELECT * FROM tbl_user WHERE id = :id", {"id": 5)
"""