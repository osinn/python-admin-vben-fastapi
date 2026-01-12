from fastapi import APIRouter, Depends

from apps.modules.sys.basis.crud.crud_sys_dept import CrudSysDept
from apps.modules.sys.basis.models.sys_dept import SysDeptModel
from apps.modules.sys.basis.params.sys_dept import SysDeptAddParam, SysDeptEditParam
from core.common.param import ChangeStatusParam
from core.framework.auth import PreAuthorize
from core.framework.crud_async_session import AsyncGenericCRUD, crud_getter
from core.framework.response import SuccessResponse, ErrorResponse

dept_router = APIRouter(prefix="/dept")


@dept_router.post("/add", summary="新增部门")
async def add(sys_dept_add_param: SysDeptAddParam,
              crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysDeptModel))):
    await crud_async_session.create(sys_dept_add_param)
    return SuccessResponse("OK")

@dept_router.put("/edit", summary="编辑部门")
async def edit(sys_dept_edit_param: SysDeptEditParam,
               crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysDeptModel))):
    db_obj = await crud_async_session.get(sys_dept_edit_param.id)
    if not db_obj:
        return ErrorResponse("部门不存在")
    await crud_async_session.update(sys_dept_edit_param, db_obj)
    return SuccessResponse("OK")

@dept_router.delete("/{dept_id}/delete_dept", summary="删除部门")
async def delete_dept(dept_id: int,
               crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysDeptModel))):
    result: bool = await crud_async_session.delete(dept_id)
    if not result:
        return ErrorResponse("删除失败")
    return SuccessResponse("OK")

@dept_router.get("/get_dept_list_all", summary="获取全部部门")
async def get_dept_list_all(crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysDeptModel))):
    model_info_all = await crud_async_session.get_model_info_all()
    return SuccessResponse(model_info_all)

@dept_router.put("/sys_dept_change_status", summary="修改岗位状态")
async def sys_dept_change_status(change_status_param: ChangeStatusParam,
                         crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysDeptModel)),
                         _=Depends(PreAuthorize(permissions=["system:dept:changeStatus"]))
                         ):
    result: bool = await crud_async_session.change_status(change_status_param.id, change_status_param.status)
    if not result:
        return ErrorResponse("状态更新失败")
    return SuccessResponse("OK")

@dept_router.get("/get_dept_all_tree", summary="查询所有部门树以及返回部门负责任人")
async def get_dept_all_tree(crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysDeptModel))):
    await CrudSysDept.get_dept_all_tree(True, crud_async_session)
    return SuccessResponse("OK")

@dept_router.get("/get_simple_dept_all_tree", summary="查询所有部门树不返回设置部门负责任")
async def get_simple_dept_all_tree(crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysDeptModel))):
    await CrudSysDept.get_dept_all_tree(False, crud_async_session)
    return SuccessResponse("OK")
