from fastapi import APIRouter, Depends, Path

from apps.modules.sys.basis.crud.crud_sys_dict_item import get_dict_item_list_all_of_dict_id
from apps.modules.sys.basis.models.sys_dict_item import SysDictItemModel
from apps.modules.sys.basis.params.sys_dict_item import SysDictItemAddParam, SysDictItemEditParam
from core.framework.auth import PreAuthorize
from core.framework.crud_async_session import AsyncGenericCRUD, crud_getter
from core.framework.response import SuccessResponse, ErrorResponse

dict_item_router = APIRouter(prefix="/dict_item")

@dict_item_router.get("/{dict_id}/get_dict_item_list_all_by_dict_id", summary="获取字典关联字典项")
async def get_dict_item_list_all_by_dict_id(dict_id: int = Path(description="字典ID"),
                        crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysDictItemModel))
                        ):
    await get_dict_item_list_all_of_dict_id(dict_id, crud_async_session)
    return SuccessResponse("OK")

@dict_item_router.post("/add", summary="新增字典项")
async def add(sys_dict_item_add_param: SysDictItemAddParam,
                        crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysDictItemModel)),
                        _ = Depends(PreAuthorize(permissions=["system:dictItem:add"]))
                        ):
    await crud_async_session.create(sys_dict_item_add_param)
    return SuccessResponse("OK")

@dict_item_router.put("/edit", summary="编辑字典项")
async def edit(sys_dict_item_edit_param: SysDictItemEditParam,
                        crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysDictItemModel)),
                        _ = Depends(PreAuthorize(permissions=["system:dictItem:edit"]))
                        ):
    db_obj = await crud_async_session.get(sys_dict_item_edit_param.id)
    if not db_obj:
        return ErrorResponse("字典不存在")
    await crud_async_session.update(sys_dict_item_edit_param, db_obj)
    return SuccessResponse("OK")


@dict_item_router.delete("/{dict_id}/delete_dict_item", summary="删除字典项")
async def delete_dict_item(dict_id: int = Path(description="字典项唯一ID"),
                      crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysDictItemModel)),
                      _ = Depends(PreAuthorize(permissions=["system:dictItem:delete"]))
                      ):
    result: bool = await crud_async_session.delete(dict_id)
    if not result:
        return ErrorResponse("删除失败")
    return SuccessResponse("OK")