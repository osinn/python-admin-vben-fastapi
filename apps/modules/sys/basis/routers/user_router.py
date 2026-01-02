from fastapi import APIRouter, Depends, Path, Body
from sqlalchemy.ext.asyncio import AsyncSession

from apps.modules.sys.basis.models.sys_user import SysUserModel
from apps.modules.sys.basis.schemas.sys_user import SysUserSchema, SysUserAddSchema
from core.framework.crud_async_session import crud_getter, AsyncGenericCRUD
from core.framework.database import db_getter
from core.framework.response import SuccessResponse
from core.framework.sql_alchemy_helper import SQLAlchemyHelper

user_router = APIRouter()

@user_router.get("/{user_id}/get_user_by_id", summary="获取用户列表")
async def get_user_list(user_id: int = Path(description="用户唯一ID"),
# name: str = Query(None, description="用户名称"),
                        db: AsyncSession = Depends(db_getter)):
    result = await SQLAlchemyHelper.select_records(db, SysUserModel, {'id': user_id}, v_schema=SysUserSchema)
    return SuccessResponse(result)


@user_router.post("/user/add", summary="添加用户")
async def create_user(sys_user_add_schema: SysUserAddSchema, crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysUserModel))):
    # 保存用户信息
    await crud_async_session.create(sys_user_add_schema)
    return SuccessResponse("OK")

