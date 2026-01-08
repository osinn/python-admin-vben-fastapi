from fastapi import APIRouter, Depends, Path

from apps.modules.sys.basis.models.sys_menu import SysMenuModel
from apps.modules.sys.basis.params.sys_menu import SysMenuAddParam, SysMenuEditParam
from core.framework.auth import AuthValidation
from core.framework.crud_async_session import crud_getter, AsyncGenericCRUD
from core.framework.database import db_getter
from core.framework.response import SuccessResponse, ErrorResponse
from core.framework.sql_alchemy_helper import SQLAlchemyHelper

menu_router = APIRouter(prefix="/menu")

@menu_router.post("/add", summary="添加菜单")
async def create_menu(sys_menu_add_schema: SysMenuAddParam, crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysMenuModel))):
    # 保存菜单信息
    if sys_menu_add_schema.password:
        sys_menu_add_schema.password = AuthValidation.get_password_hash(sys_menu_add_schema.password)
    await crud_async_session.create(sys_menu_add_schema)
    return SuccessResponse("OK")

@menu_router.put("/edit", summary="编辑菜单")
async def edit_menu(sys_menu_edit_schema: SysMenuEditParam, crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysMenuModel))):
    db_obj = await crud_async_session.get(sys_menu_edit_schema.id)
    if not db_obj:
        return ErrorResponse("菜单不存在")
    await crud_async_session.update(sys_menu_edit_schema, db_obj)
    return SuccessResponse("OK")

@menu_router.delete("/{menu_id}/delete_menu", summary="删除菜单")
async def delete_menu(menu_id: int = Path(description="菜单唯一ID"),
                      crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysMenuModel))):
    result = await crud_async_session.delete(menu_id)
    if not result:
        return ErrorResponse("删除失败")
    return SuccessResponse("OK")
