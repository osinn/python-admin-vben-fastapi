import re
from typing import Type, Optional, List, Any

from fastapi import Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text, update, insert
from pydantic import BaseModel

from core.framework.common_schemas import PageVo
from core.framework.database import db_getter

class AsyncGenericCRUD:
    def __init__(self, user, model_class: Type, db: AsyncSession):
        self.model_class = model_class
        self.db: AsyncSession = db  # 将由依赖注入赋值
        self.user = user  # 将由依赖注入赋值

    async def first_model(
            self,
            sql: str,
            params: dict = None,
            model_class: Type = None,
    ) -> Optional[object]:
        """
        执行SQL查询返回第一个模型对象
        :param sql: 执行SQL
        :param params: 查询参数
        :return:
        """
        result = await self.db.execute(text(sql), params or {})
        if model_class:
            row = result.mappings().first()
            return model_class(**row) if row else None
        else:
            return result.scalar_one_or_none()

    async def list_model(
            self,
            sql: str,
            params: dict = None,
            v_schema: Any = None
    ) -> list:
        """
        执行SQL查询返回第一个模型对象
        sql 动态参数判断
            sql = (f"select * from tbl_sys_user where is_deleted = false"
                    f"{" and status =: status" if sys_user_page_param.status else ''}" # 如果 status 不为空则参与查询
                    f"{" and name =: search_key" if sys_user_page_param.search_key else ''}" # 如果 search_key 不为空则参与查询
                )
        :param sql: 执行SQL
        :param params: 查询参数
        :param v_schema: 序列化对象
        :return: 返回一个行字典集合
        """
        """
        添加过滤条件
        :param sql:
        :param kwargs: 关键词参数
        """
        result = await self.db.execute(text(sql), params or {})
        rows = result.fetchall()
        if rows and v_schema:
            # return [v_schema.model_validate(obj._mapping).model_dump() for obj in rows]
            return [v_schema(**v_schema.model_validate(obj).model_dump()) for obj in rows]
        else:
            return [dict(row._mapping) for row in rows]

    async def page_select_model(
            self,
            sql: str,
            params: dict = None,
            v_schema: Any = None
    ) -> Optional[object]:
        """
        执行SQL查询返回第一个模型对象
        sql 动态参数判断
            sql = (f"select * from tbl_sys_user where is_deleted = false"
                    f"{" and status =: status" if sys_user_page_param.status else ''}" # 如果 status 不为空则参与查询
                    f"{" and name =: search_key" if sys_user_page_param.search_key else ''}" # 如果 search_key 不为空则参与查询
                )
        :param sql: 执行SQL
        :param params: 查询参数
        :return:
        """
        """
        添加过滤条件
        :param sql:
        :param kwargs: 关键词参数
        :param v_schema: 序列化对象
        """
        count_sql = re.sub(
            r'^\s*SELECT\s+.*?\s+FROM\s',
            'SELECT COUNT(1) FROM ',
            sql,
            flags=re.IGNORECASE | re.DOTALL
        )

        count_sql = re.split(r'\s+ORDER\s+BY\s', count_sql, flags=re.IGNORECASE)[0]

        count_sql = re.split(r'\s+(LIMIT|OFFSET)\s', count_sql, flags=re.IGNORECASE)[0].strip()

        count_result = await self.db.execute(text(count_sql), params or {})
        total = count_result.scalar_one()
        result = await self.db.execute(text(sql), params or {})
        rows = result.fetchall()

        if rows and v_schema:
            return PageVo(total, [v_schema(**v_schema.model_validate(obj).model_dump()) for obj in rows])
        else:
            return PageVo(total, rows if rows else [])

    async def bulk_update_fields(self, record_id: int, **fields) -> bool:
        """
        通用更新字段
        :param id 唯一ID
        :param fields 所需要更新的字段，例如：bulk_update_fields(123, updated_by=456, status=1)
        :return 如果更新成功 返回True, 否则返回False
        """
        result = await self.db.execute(
            update(self.model_class)
            .where(self.model_class.id == record_id)
            .values(**fields)
        )
        return result.rowcount > 0

    async def bulk_insert(self,data_list: list[dict], table = None):
        """
        插入数据
        :param data_list: 需要插入的数据 [{field:value}]
        :param table: 表 如果不指定，使用对应注入的模型表
        :return:
        """
        if not data_list:
            return
        stmt = insert(table if table is not None else self.model_class).values(data_list)
        await self.db.execute(stmt)

    async def change_status(self, id: int, status: int) -> bool:
        """
        更新状态值
        :param id 唯一ID
        :param status 状态值
        :return 如果更新成功 返回True, 否则返回False
        """
        result = await self.db.execute(
            update(self.model_class)
            .where(self.model_class.id == id)
            .values(status = status, updated_by = self.user["id"])
        )
        return result.rowcount > 0

    async def change_sort(self, id: int, sort: int) -> bool:
        """
        更新排序值
        :param id 唯一ID
        :param sort 状态值
        :return 如果更新成功 返回True, 否则返回False
        """
        result = await self.db.execute(
            update(self.model_class)
            .where(self.model_class.id == id)
            .values(sort = sort, updated_by = self.user["id"])
        )
        return result.rowcount > 0

    async def execute_sql(self, sql: str, params: dict = None, fetch_data: bool = False):
        if fetch_data:
            result = await self.db.execute(text(sql), params or {})
            result_data = result.mappings().all()
            return [dict(row) for row in result_data]
        else:
            await self.db.execute(text(sql), params or {})
            return None

    async def get(self, id: int):
        result = await self.db.execute(
            select(self.model_class).where(self.model_class.id == id)
        )
        return result.scalar_one_or_none()


    async def get_model_info_all(self, v_schema = None) -> Optional[Any]:
        """
        查询 model 所有非删除数据
        :param v_schema 指定序列化
        :return: 如果指定，则序列化后返回 v_schema 对象集合，否则返回 model 对象集合
        """
        result = await self.db.execute(
            select(self.model_class).where(self.model_class.is_deleted == False)
        )
        rows = result.scalars().all()
        if v_schema:
            return [v_schema(**v_schema.model_validate(obj).model_dump()) for obj in rows]
        else:
            return rows

    async def get_multi(self, skip: int = 0, limit: int = 100) -> List[object]:
        stmt = select(self.model_class).offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create(self, obj_in: BaseModel) -> object:
        """
        Field(exclude=True) 如果字段不在 ORM模型中，需要在Field中将exclude设置为 True排出此字段，否则不会报错
        :param obj_in:
        :return:
        """
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
        update_data = obj_in.model_dump()
        user = self.user
        if user and user.get("id", None) is not None:
            update_data["updated_by"] = user.get("id", None)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        await self.db.flush()
        return db_obj

    async def update(self, obj_in: BaseModel, db_obj) -> Optional[object]:
        update_data = obj_in.model_dump()
        user = self.user
        if user and user.get("id", None) is not None:
            update_data["updated_by"] = user.get("id", None)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        await self.db.flush()
        return db_obj

    async def delete(self, id: int, logic_delete: bool = True) -> bool:
        """
        删除数据
        :param id: 记录ID
        :param logic_delete: 是否逻辑删除，默认是
        :return:
        """
        db_obj = await self.get(id)
        if not db_obj:
            return False
        if logic_delete:
            db_obj.is_deleted = True
        else:
            await self.db.delete(db_obj)
        return True

def crud_getter(model_class: Type):
    """
    返回一个依赖函数，用于注入绑定当前 db 会话的 AsyncGenericCRUD 实例
    """
    async def _get_crud(request: Request, db: AsyncSession = Depends(db_getter)) -> AsyncGenericCRUD:
        user = getattr(request.state, "user", None)
        crud = AsyncGenericCRUD(user, model_class=model_class, db=db)
        return crud
    return _get_crud