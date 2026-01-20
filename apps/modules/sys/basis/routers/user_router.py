from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from apps.modules.sys.basis.crud.crud_sys_user import CrudSysUser
from apps.modules.sys.basis.models.sys_user import SysUserModel
from apps.modules.sys.basis.models.sys_user_post import SysUserPostModel
from apps.modules.sys.basis.models.sys_user_role import SysUserRoleModel
from apps.modules.sys.basis.params.sys_user import SysUserAddParam, SysUserEditParam, SysUserPageParam, \
    SysUserResetPwdParam
from apps.modules.sys.basis.schemas.sys_user import SysUserSchema
from core.common.param import ChangeStatusParam
from core.framework.auth import AuthValidation, PreAuthorize
from core.framework.crud_async_session import crud_getter, AsyncGenericCRUD
from core.framework.database import db_getter
from core.framework.response import SuccessResponse, ErrorResponse
from core.framework.sql_alchemy_helper import SQLAlchemyHelper

user_router = APIRouter(prefix="/user")

@user_router.post("/get_user_list", summary="获取用户列表")
async def get_user_list(sys_user_page_param: SysUserPageParam,
                        crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysUserModel))
                        ):
    page_vo = await CrudSysUser.page_query_user_list(sys_user_page_param, crud_async_session)
    await CrudSysUser.fill_base_user_info(page_vo.items, crud_async_session)
    await CrudSysUser.fill_user_data(page_vo.items,crud_async_session)
    return SuccessResponse(page_vo)

@user_router.get("/{user_id}/get_user_by_id", summary="获取用户详情")
async def get_user_info(user_id: int = Path(description="用户唯一ID"),
                        db: AsyncSession = Depends(db_getter), crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysUserModel))):
    result = await SQLAlchemyHelper.select_records(db, SysUserModel, {'id': user_id}, v_schema=SysUserSchema)
    return SuccessResponse(result)

@user_router.post("/add_user", summary="添加用户")
async def create_user(sys_user_add_schema: SysUserAddParam, crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysUserModel)),
                      _ = Depends(PreAuthorize(permissions=["system:user:add"]))
                      ):
    # 保存用户信息
    if sys_user_add_schema.password:
        sys_user_add_schema.password = AuthValidation.get_password_hash(sys_user_add_schema.password)

    is_unique_email: bool = await CrudSysUser.check_unique_email(sys_user_add_schema.email, None,crud_async_session)
    if is_unique_email:
        return ErrorResponse("邮箱已存在")

    is_unique_staff_number: bool = await CrudSysUser.check_unique_staff_number(sys_user_add_schema.staff_number, None, crud_async_session)
    if is_unique_staff_number:
        return ErrorResponse("员工编号已存在")

    db_obj = await crud_async_session.create(sys_user_add_schema)


    if sys_user_add_schema.role_ids:
        roles = [SysUserRoleModel(user_id=db_obj.id, role_id=role_id) for role_id in
                 sys_user_add_schema.role_ids]
        crud_async_session.db.add_all(roles)

    if sys_user_add_schema.post_ids:
        posts = [SysUserPostModel(user_id=db_obj.id, post_id=post_id) for post_id in
                 sys_user_add_schema.post_ids]
        crud_async_session.db.add_all(posts)

    return SuccessResponse("OK")

@user_router.put("/edit_user", summary="编辑用户")
async def edit_user(sys_user_edit_schema: SysUserEditParam, crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysUserModel)),
                    _ = Depends(PreAuthorize(permissions=["system:user:edit"]))
                    ):
    db_obj = await crud_async_session.get(sys_user_edit_schema.id)
    if not db_obj:
        return ErrorResponse("用户不存在")
    if sys_user_edit_schema.password:
        sys_user_edit_schema.password = AuthValidation.get_password_hash(sys_user_edit_schema.password)

    is_unique_email: bool = await CrudSysUser.check_unique_email(sys_user_edit_schema.email, sys_user_edit_schema.id, crud_async_session)
    if is_unique_email:
        return ErrorResponse("邮箱已存在")

    is_unique_staff_number: bool = await CrudSysUser.check_unique_staff_number(sys_user_edit_schema.staff_number, sys_user_edit_schema.id, crud_async_session)
    if is_unique_staff_number:
        return ErrorResponse("员工编号已存在")

    await CrudSysUser.delete_user_post_and_role_of_user_id(sys_user_edit_schema.id, crud_async_session)

    sql = "delete from tbl_sys_user_role where user_id = :user_id"
    await crud_async_session.execute_sql(sql, {"user_id": sys_user_edit_schema.id})

    sql = "delete from tbl_sys_user_post where user_id = :user_id"
    await crud_async_session.execute_sql(sql, {"user_id": sys_user_edit_schema.id})

    if sys_user_edit_schema.role_ids:
       roles = [SysUserRoleModel(user_id = sys_user_edit_schema.id, role_id = role_id) for role_id in sys_user_edit_schema.role_ids]
       crud_async_session.db.add_all(roles)
    if sys_user_edit_schema.post_ids:
       posts = [SysUserPostModel(user_id = sys_user_edit_schema.id, post_id = post_id) for post_id in sys_user_edit_schema.post_ids]
       crud_async_session.db.add_all(posts)

    await crud_async_session.update(sys_user_edit_schema, db_obj)
    return SuccessResponse("OK")

@user_router.delete("/{user_id}/delete_user", summary="删除用户")
async def delete_user(user_id: int = Path(description="用户唯一ID"),
                      crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysUserModel)),
                      _ = Depends(PreAuthorize(permissions=["system:user:delete"]))
                      ):
    result: bool = await crud_async_session.delete(user_id)
    if not result:
        return ErrorResponse("删除失败")
    return SuccessResponse("OK")

@user_router.get("/get_user_list_all", summary="查询全部用户")
async def get_user_list_all(crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysUserModel))):
    model_info_all = await crud_async_session.get_model_info_all(v_schema=SysUserSchema)
    return SuccessResponse(model_info_all)

@user_router.put("/sys_user_reset_pwd", summary="重置密码")
async def sys_user_reset(sys_user_reset_pwd_param: SysUserResetPwdParam, crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysUserModel)),
                         _ = Depends(PreAuthorize(permissions=["system:user:resetPwd"]))
                         ):
    user_info = await crud_async_session.get(sys_user_reset_pwd_param.id)
    if user_info is None:
        return ErrorResponse("用户不存在")
    user = crud_async_session.user
    new_password = AuthValidation.get_password_hash(sys_user_reset_pwd_param.password)
    result: bool = await crud_async_session.bulk_update_fields(sys_user_reset_pwd_param.id, password=new_password, updated_by = user["id"])
    if not result:
        return ErrorResponse("重置密码失败")
    return SuccessResponse("OK")

@user_router.put("/sys_user_change_status", summary="修改用户状态")
async def sys_user_reset(change_status_param: ChangeStatusParam, crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysUserModel)),
                         _ = Depends(PreAuthorize(permissions=["system:user:changeStatus"]))
                         ):
    result: bool = await crud_async_session.change_status(change_status_param.id, change_status_param.status)
    if not result:
        return ErrorResponse("状态更新失败")
    return SuccessResponse("OK")
