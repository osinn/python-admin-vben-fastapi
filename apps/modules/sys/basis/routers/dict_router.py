from fastapi import APIRouter, Depends, Path

from apps.modules.sys.basis.crud.crud_sys_dict import get_page_dict_list
from apps.modules.sys.basis.models.sys_dict import SysDictModel
from apps.modules.sys.basis.params.sys_dict import SysDictPageParam, SysDictAddParam, SysDictEditParam
from core.common.param import ChangeStatusParam
from core.framework.auth import PreAuthorize
from core.framework.crud_async_session import AsyncGenericCRUD, crud_getter
from core.framework.response import SuccessResponse, ErrorResponse

dict_router = APIRouter(prefix="/dict")

@dict_router.post("/get_dict_list", summary="获取字典列表")
async def get_dict_list(sys_dict_page_param: SysDictPageParam,
                        crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysDictModel))
                        ):
    page_vo = await get_page_dict_list(sys_dict_page_param, crud_async_session)
    return SuccessResponse(page_vo)

@dict_router.post("/add", summary="新增字典")
async def add(sys_dict_add_param: SysDictAddParam,
                        crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysDictModel)),
                        _ = Depends(PreAuthorize(permissions=["system:dict:add"]))
                        ):
    await crud_async_session.create(sys_dict_add_param)
    return SuccessResponse("OK")

@dict_router.put("/edit", summary="编辑字典")
async def edit(sys_dict_edit_param: SysDictEditParam,
                        crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysDictModel)),
                        _ = Depends(PreAuthorize(permissions=["system:dict:edit"]))
                        ):
    db_obj = await crud_async_session.get(sys_dict_edit_param.id)
    if not db_obj:
        return ErrorResponse("字典不存在")
    await crud_async_session.update(sys_dict_edit_param, db_obj)
    return SuccessResponse("OK")


@dict_router.delete("/{dict_id}/delete_dict", summary="删除字典")
async def delete_dict(dict_id: int = Path(description="字典唯一ID"),
                      crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysDictModel)),
                      _ = Depends(PreAuthorize(permissions=["system:dict:delete"]))
                      ):
    result: bool = await crud_async_session.delete(dict_id)
    if not result:
        return ErrorResponse("删除失败")
    return SuccessResponse("OK")

@dict_router.put("/dict_change_status", summary="修改用户状态")
async def dict_change_status(change_status_param: ChangeStatusParam, crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysDictModel)),
                         _ = Depends(PreAuthorize(permissions=["system:dict:changeStatus"]))
                         ):
    result: bool = await crud_async_session.change_status(change_status_param.id, change_status_param.status)
    if not result:
        return ErrorResponse("状态更新失败")
    return SuccessResponse("OK")
