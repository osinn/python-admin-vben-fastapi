from fastapi import APIRouter, Depends, Path
from sqlalchemy import select, exists

from apps.modules.sys.basis.crud.crud_sys_menu import CrudSysMenu
from apps.modules.sys.basis.models.sys_menu import SysMenuModel
from apps.modules.sys.basis.params.sys_menu import SysMenuAddParam, SysMenuEditParam, SysMenuCheckExistsParam
from core.common.param import ChangeSortParam
from core.framework.auth import PreAuthorize
from core.framework.crud_async_session import crud_getter, AsyncGenericCRUD
from core.framework.response import SuccessResponse, ErrorResponse

menu_router = APIRouter(prefix="/menu")


@menu_router.post("/name-exists", summary="检查菜单名称是否存在")
async def name_exists(sys_menu_check_exists_schema: SysMenuCheckExistsParam,
                      crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysMenuModel))):
    stmt = select(exists().where(SysMenuModel.name == sys_menu_check_exists_schema.key))
    result = await crud_async_session.db.execute(stmt)
    result_value = result.scalar()
    return SuccessResponse(result_value)


@menu_router.post("/path-exists", summary="检查菜单路径是否存在")
async def path_exists(sys_menu_check_exists_schema: SysMenuCheckExistsParam,
                      crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysMenuModel))):
    stmt = select(exists().where(SysMenuModel.path == sys_menu_check_exists_schema.key))
    result = await crud_async_session.db.execute(stmt)
    result_value = result.scalar()
    return SuccessResponse(result_value)


@menu_router.post("/add", summary="添加菜单")
async def create_menu(sys_menu_add_schema: SysMenuAddParam,
                      crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysMenuModel)),
                      _ = Depends(PreAuthorize(permissions=["system:menu:add"]))
                      ):
    await crud_async_session.create(sys_menu_add_schema)
    return SuccessResponse("OK")


@menu_router.put("/edit", summary="编辑菜单")
async def edit_menu(sys_menu_edit_schema: SysMenuEditParam,
                    crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysMenuModel)),
                    _ = Depends(PreAuthorize(permissions=["system:menu:edit"]))
                    ):
    db_obj = await crud_async_session.get(sys_menu_edit_schema.id)
    if not db_obj:
        return ErrorResponse("菜单不存在")
    await crud_async_session.update(sys_menu_edit_schema, db_obj)
    return SuccessResponse("OK")


@menu_router.delete("/{menu_id}/delete_menu", summary="删除菜单")
async def delete_menu(menu_id: int = Path(description="菜单唯一ID"),
                      crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysMenuModel)),
                      _ = Depends(PreAuthorize(permissions=["system:menu:delete"]))
                      ):
    result = await crud_async_session.delete(menu_id)
    if not result:
        return ErrorResponse("删除失败")
    await crud_async_session.execute_sql(f"DELETE FROM tbl_sys_role_menu WHERE menu_id = {menu_id}")
    return SuccessResponse("OK")


@menu_router.get("/get_menu_tree_list_all", summary="获取树形菜单")
async def get_menu_tree_list_all(crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysMenuModel))):
    route_item = await CrudSysMenu.get_menu_tree_list_all(crud_async_session)
    return SuccessResponse(route_item)


@menu_router.get("/get_assignment_permission_ids_by_role_id/{role_id}", summary="获取角色已分配的权限ID列表")
async def get_assignment_permission_ids_by_role_id(role_id: int = Path(description="角色唯一ID"),
                                                   crud_async_session: AsyncGenericCRUD = Depends(
                                                       crud_getter(SysMenuModel))):
    route_item = await CrudSysMenu.get_assignment_permission_ids_by_role_id(role_id, crud_async_session)
    return SuccessResponse(route_item)


@menu_router.put("/change_menu_sort", summary="更改菜单排序")
async def change_menu_sort(change_sort_param: ChangeSortParam,
                           crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysMenuModel)),
                           _ = Depends(PreAuthorize(permissions=["system:menu:changeSort"]))
                           ):
    result: bool = await crud_async_session.change_sort(change_sort_param.id, change_sort_param.sort)
    if not result:
        return ErrorResponse("更改菜单排序失败")
    return SuccessResponse("OK")
