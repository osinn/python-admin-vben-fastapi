from typing import Type, Optional, List

from fastapi import Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text, func, BinaryExpression
from pydantic import BaseModel

from core.framework.database import db_getter
from core.framework.exception import SqlException


class AsyncGenericCRUD:
    def __init__(self, user, model_class: Type, db: AsyncSession):
        self.model_class = model_class
        self.db: AsyncSession = db  # 将由依赖注入赋值
        self.user = user  # 将由依赖注入赋值

    async def first_model(
            self,
            sql: str,
            params: dict = None
    ) -> Optional[object]:
        """
        执行SQL查询返回第一个模型对象
        :param sql: 执行SQL
        :param params: 查询参数
        :return:
        """
        result = await self.db.execute(text(sql), params or {})
        return result.scalar_one_or_none()

    async def list_model(
            self,
            sql: str,
            params: dict = None
    ) -> Optional[object]:
        """
        执行SQL查询返回第一个模型对象
        :param sql: 执行SQL
        :param params: 查询参数
        :return:
        """
        """
        添加过滤条件
        :param sql:
        :param kwargs: 关键词参数
        """
        result = await self.db.execute(text(sql), params or {})
        return result.fetchall()

    async def get(self, id: int) -> Optional[object]:
        result = await self.db.execute(
            select(self.model_class).where(self.model_class.id == id)
        )
        return result.scalar_one_or_none()

    async def get_multi(self, skip: int = 0, limit: int = 100) -> List[object]:
        stmt = select(self.model_class).offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create(self, obj_in: BaseModel) -> object:
        obj_data = obj_in.model_dump()

        user = self.user
        if user and user.get("id", None) is not None:
            obj_data["created_by"] = user.get("id", None)
        db_obj = self.model_class(**obj_data)
        self.db.add(db_obj)
        await self.db.flush()
        return db_obj

    async def update_by_id(self, id: int, obj_in: BaseModel) -> Optional[object]:
        db_obj = await self.get(id)
        if not db_obj:
            return None
        update_data = obj_in.model_dump(exclude_unset=True)
        user = self.user
        if user and user.get("id", None) is not None:
            update_data["updated_by"] = user.get("id", None)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        await self.db.flush()
        return db_obj

    async def update(self, obj_in: BaseModel, db_obj) -> Optional[object]:
        update_data = obj_in.model_dump(exclude_unset=True)
        user = self.user
        if user and user.get("id", None) is not None:
            update_data["updated_by"] = user.get("id", None)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        await self.db.flush()
        return db_obj

    async def delete(self, id: int) -> bool:
        db_obj = await self.get(id)
        if not db_obj:
            return False
        await self.db.delete(db_obj)
        return True
    def __dict_filter(self, **kwargs) -> list[BinaryExpression]:
        """
        字典过滤
        :param model:
        :param kwargs:
        """
        conditions = []
        for field, value in kwargs.items():
            if value is not None and value != "":
                attr = getattr(self.model, field)
                if isinstance(value, tuple):
                    if len(value) == 1:
                        if value[0] == "None":
                            conditions.append(attr.is_(None))
                        elif value[0] == "not None":
                            conditions.append(attr.isnot(None))
                        else:
                            raise SqlException("SQL查询语法错误")
                    elif len(value) == 2 and value[1] not in [None, [], ""]:
                        if value[0] == "date":
                            # 根据日期查询， 关键函数是：func.time_format和func.date_format
                            conditions.append(func.date_format(attr, "%Y-%m-%d") == value[1])
                        elif value[0] == "like":
                            conditions.append(attr.like(f"%{value[1]}%"))
                        elif value[0] == "in":
                            conditions.append(attr.in_(value[1]))
                        elif value[0] == "between" and len(value[1]) == 2:
                            conditions.append(attr.between(value[1][0], value[1][1]))
                        elif value[0] == "month":
                            conditions.append(func.date_format(attr, "%Y-%m") == value[1])
                        elif value[0] == "!=":
                            conditions.append(attr != value[1])
                        elif value[0] == ">":
                            conditions.append(attr > value[1])
                        elif value[0] == ">=":
                            conditions.append(attr >= value[1])
                        elif value[0] == "<=":
                            conditions.append(attr <= value[1])
                        else:
                            raise SqlException("SQL查询语法错误")
                else:
                    conditions.append(attr == value)
        return conditions


def crud_getter(model_class: Type):
    """
    返回一个依赖函数，用于注入绑定当前 db 会话的 AsyncGenericCRUD 实例
    """
    async def _get_crud(request: Request, db: AsyncSession = Depends(db_getter)) -> AsyncGenericCRUD:
        user = getattr(request.state, "user", None)
        crud = AsyncGenericCRUD(user, model_class=model_class, db=db)
        return crud
    return _get_crud