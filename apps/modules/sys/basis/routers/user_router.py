from fastapi import APIRouter, Depends, Path
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from apps.modules.sys.basis.crud.crud_sys_user import CrudSysUser
from apps.modules.sys.basis.models.sys_user import SysUserModel
from apps.modules.sys.basis.params.sys_user import SysUserAddParam, SysUserEditParam, SysUserPageParam, \
    SysUserResetPwdParam
from apps.modules.sys.basis.schemas.sys_user import SysUserSchema
from core.framework.auth import AuthValidation, PreAuthorize
from core.framework.crud_async_session import crud_getter, AsyncGenericCRUD
from core.framework.database import db_getter
from core.framework.response import SuccessResponse, ErrorResponse
from core.framework.sql_alchemy_helper import SQLAlchemyHelper
from core.utils.JSONUtils import JSONUtils

user_router = APIRouter(prefix="/user")

@user_router.post("/get_user_list", summary="获取用户列表")
async def get_user_list(sys_user_page_param: SysUserPageParam,
                        crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysUserModel)),
                        _ = Depends(PreAuthorize(permissions=["sys:demo"])) # 需要有 sys:demo 权限才能访问
                        ):
    page_vo = await CrudSysUser.page_query_user_list(sys_user_page_param, crud_async_session)
    return SuccessResponse(page_vo)

@user_router.get("/{user_id}/get_user_by_id", summary="获取用户详情")
async def get_user_info(user_id: int = Path(description="用户唯一ID"),
                        db: AsyncSession = Depends(db_getter), crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysUserModel))):
    result = await SQLAlchemyHelper.select_records(db, SysUserModel, {'id': user_id}, v_schema=SysUserSchema)
    data = await CrudSysUser.get_sys_user_permission(user_id, crud_async_session)
    print(JSONUtils.dumps(data))
    return SuccessResponse(result)

@user_router.post("/add", summary="添加用户")
async def create_user(sys_user_add_schema: SysUserAddParam, crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysUserModel))):
    # 保存用户信息
    if sys_user_add_schema.password:
        sys_user_add_schema.password = AuthValidation.get_password_hash(sys_user_add_schema.password)
    await crud_async_session.create(sys_user_add_schema)
    return SuccessResponse("OK")

@user_router.put("/edit", summary="编辑用户")
async def edit_user(sys_user_edit_schema: SysUserEditParam, crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysUserModel))):
    db_obj = await crud_async_session.get(sys_user_edit_schema.id)
    if not db_obj:
        return ErrorResponse("用户不存在")
    if sys_user_edit_schema.password:
        sys_user_edit_schema.password = AuthValidation.get_password_hash(sys_user_edit_schema.password)
    await crud_async_session.update(sys_user_edit_schema, db_obj)
    return SuccessResponse("OK")

@user_router.delete("/{user_id}/delete_user", summary="删除用户")
async def delete_user(user_id: int = Path(description="用户唯一ID"),
                      crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysUserModel))):
    result = await crud_async_session.delete(user_id)
    if not result:
        return ErrorResponse("删除失败")
    return SuccessResponse("OK")

@user_router.post("/get_user_list_all", summary="查询全部用户")
async def get_user_list_all(crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysUserModel))):
    model_info_all = await crud_async_session.get_model_info_all(v_schema=SysUserSchema)
    return SuccessResponse(model_info_all)

@user_router.post("/get_user_list_all", summary="重置密码")
async def get_user_list_all(sys_user_reset_pwd_param: SysUserResetPwdParam, crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysUserModel))):
    user_info = await crud_async_session.get(sys_user_reset_pwd_param.id)
    if user_info is None:
        return ErrorResponse("用户不存在")

    new_password = AuthValidation.get_password_hash(sys_user_reset_pwd_param.new_password)
    # update(SysUserModel).where(and_(SysUserModel.id == sys_user_reset_pwd_param.id))
    # await crud_async_session.db.execute()
    return SuccessResponse("OK")
