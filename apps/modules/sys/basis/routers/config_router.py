from fastapi import APIRouter, Depends, Path

from apps.modules.sys.basis.crud.crud_sys_config import get_page_config_list
from apps.modules.sys.basis.models.sys_config import SysConfigModel
from apps.modules.sys.basis.params.sys_config import SysConfigPageParam, SysConfigAddParam, SysConfigEditParam
from core.common.param import ChangeStatusParam
from core.framework.auth import PreAuthorize
from core.framework.crud_async_session import AsyncGenericCRUD, crud_getter
from core.framework.response import SuccessResponse, ErrorResponse

sys_config_router = APIRouter(prefix="/config")

@sys_config_router.post("/get_config_list", summary="获取系统参数列表")
async def get_config_list(sys_config_page_param: SysConfigPageParam,
                        crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysConfigModel))
                        ):
    page_vo = await get_page_config_list(sys_config_page_param, crud_async_session)
    return SuccessResponse(page_vo)

@sys_config_router.post("/add", summary="新增系统参数")
async def get_config_list(sys_config_add_param: SysConfigAddParam,
                        crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysConfigModel)),
                        _ = Depends(PreAuthorize(permissions=["system:config:add"]))
                        ):
    await crud_async_session.create(sys_config_add_param)
    return SuccessResponse("OK")

@sys_config_router.post("/edit", summary="编辑系统参数")
async def edit(sys_config_edit_param: SysConfigEditParam,
                        crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysConfigModel)),
                        _ = Depends(PreAuthorize(permissions=["system:config:edit"]))
                        ):
    db_obj = await crud_async_session.get(sys_config_edit_param.id)
    if not db_obj:
        return ErrorResponse("系统参数不存在")
    await crud_async_session.update(sys_config_edit_param, db_obj)
    return SuccessResponse("OK")

@sys_config_router.delete("/{sys_config_id}/delete_sys_config", summary="删除系统参数")
async def delete_config(sys_config_id: int = Path(description="系统参数唯一ID"),
                      crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysConfigModel)),
                      _ = Depends(PreAuthorize(permissions=["system:config:delete"]))
                      ):
    result: bool = await crud_async_session.delete(sys_config_id)
    if not result:
        return ErrorResponse("删除失败")
    return SuccessResponse("OK")

@sys_config_router.put("/sys_config_change_status", summary="修改用户状态")
async def sys_config_change_status(change_status_param: ChangeStatusParam, crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysConfigModel)),
                         _ = Depends(PreAuthorize(permissions=["system:config:changeStatus"]))
                         ):
    result: bool = await crud_async_session.change_status(change_status_param.id, change_status_param.status)
    if not result:
        return ErrorResponse("状态更新失败")
    return SuccessResponse("OK")
