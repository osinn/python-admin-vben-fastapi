from fastapi import APIRouter, Depends, Path
from sqlalchemy import delete, insert, except_
from sqlalchemy.ext.asyncio import AsyncSession

from apps.modules.sys.basis.crud.crud_sys_role import CrudSysRole
from apps.modules.sys.basis.models.sys_role import SysRoleModel
from apps.modules.sys.basis.models.sys_role_menu import SysRoleMenuModel
from apps.modules.sys.basis.params.sys_role import SysRolePageParam, SysRoleAddParam, SysRoleEditParam, SysRoleAssignMenuParam
from apps.modules.sys.basis.schemas.sys_role import SysRoleSchema
from core.common.param import ChangeStatusParam
from core.framework.auth import PreAuthorize
from core.framework.crud_async_session import AsyncGenericCRUD, crud_getter
from core.framework.database import db_getter
from core.framework.response import SuccessResponse, ErrorResponse
from core.framework.sql_alchemy_helper import SQLAlchemyHelper

role_router = APIRouter(prefix="/role")

@role_router.post("/get_role_list", summary="获取角色列表")
async def get_role_list(sys_role_page_param: SysRolePageParam, crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysRoleModel))):
    page_vo = await CrudSysRole.page_query_role_list(sys_role_page_param, crud_async_session)
    return SuccessResponse(page_vo)

@role_router.post("/get_role_list_all", summary="查询全部角色")
async def get_role_list_all(crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysRoleModel))):
    model_info_all = await crud_async_session.get_model_info_all(v_schema=SysRoleSchema)
    return SuccessResponse(model_info_all)

@role_router.post("/add", summary="添加角色")
async def create_role(sys_role_add_schema: SysRoleAddParam, crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysRoleModel)),
                      _ = Depends(PreAuthorize(permissions=["system:role:add"]))
                      ):
    await crud_async_session.create(sys_role_add_schema)
    return SuccessResponse("OK")

@role_router.put("/edit", summary="编辑角色")
async def edit_role(sys_role_edit_schema: SysRoleEditParam, crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysRoleModel)),
                    _ = Depends(PreAuthorize(permissions=["system:role:edit"]))
                    ):
    db_obj = await crud_async_session.get(sys_role_edit_schema.id)
    if not db_obj:
        return ErrorResponse("角色不存在")
    await crud_async_session.update(sys_role_edit_schema, db_obj)
    return SuccessResponse("OK")

@role_router.delete("/{role_id}/delete_role", summary="删除角色")
async def delete_role(role_id: int = Path(description="角色唯一ID"),
                      crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysRoleModel)),
                      _ = Depends(PreAuthorize(permissions=["system:role:delete"]))
                      ):
    result = await crud_async_session.delete(role_id)
    if not result:
        return ErrorResponse("删除失败")
    return SuccessResponse("OK")

@role_router.put("/sys_role_change_status", summary="修改角色状态")
async def sys_user_reset(change_status_param: ChangeStatusParam, crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysRoleModel)),
                         _ = Depends(PreAuthorize(permissions=["system:role:changeStatus"]))
                         ):
    result: bool = await crud_async_session.change_status(change_status_param.id, change_status_param.status)
    if not result:
        return ErrorResponse("状态更新失败")
    return SuccessResponse("OK")

@role_router.get("/{role_id}/get_role_by_id", summary="获取角色详情")
async def get_role_info(role_id: int = Path(description="角色唯一ID"),
                        db: AsyncSession = Depends(db_getter)):
    result = await SQLAlchemyHelper.select_records(db, SysRoleModel, {'id': role_id}, v_schema=SysRoleSchema)
    return SuccessResponse(result)

@role_router.put("/assign_menu", summary="角色分配菜单")
async def assign_menu(sys_role_assign_menu_param: SysRoleAssignMenuParam,
                        crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysRoleModel)),
                      _ = Depends(PreAuthorize(permissions=["system:permission:assignment"]))
                      ):
    await crud_async_session.db.execute(delete(SysRoleMenuModel).where(SysRoleMenuModel.role_id == sys_role_assign_menu_param.role_id))
    menu_ids = sys_role_assign_menu_param.menu_ids
    if menu_ids:
        insert_data = [{"role_id": sys_role_assign_menu_param.role_id, "menu_id": mid} for mid in menu_ids]
        await crud_async_session.bulk_insert(insert_data, SysRoleMenuModel)
    return SuccessResponse("OK")
