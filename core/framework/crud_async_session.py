# async_crud.py
from typing import Type, Optional, List

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel

from core.framework.database import db_getter


class AsyncGenericCRUD:
    def __init__(self, model_class: Type, db: AsyncSession):
        self.model_class = model_class
        self.db: AsyncSession = db  # 将由依赖注入赋值

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
        obj_data["created_by"] = 1
        # obj_data.update({"created_by": 30, "country": "China"})
        db_obj = self.model_class(**obj_data)
        self.db.add(db_obj)
        await self.db.flush()
        return db_obj

    async def update(self, id: int, obj_in: BaseModel) -> Optional[object]:
        db_obj = await self.get(id)
        if not db_obj:
            return None
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        await self.db.flush()
        return db_obj

    async def delete(self, id: int) -> bool:
        db_obj = await self.get(id)
        if not db_obj:
            return False
        await self.db.delete(db_obj)
        await self.db.commit()
        return True

def crud_getter(model_class: Type):
    """
    返回一个依赖函数，用于注入绑定当前 db 会话的 AsyncGenericCRUD 实例
    """
    async def _get_crud(db: AsyncSession = Depends(db_getter)) -> AsyncGenericCRUD:
        crud = AsyncGenericCRUD(model_class=model_class, db=db)
        return crud
    return _get_crud