from typing import List, Optional

from fastapi import APIRouter, Depends, Query

from apps.modules.sys.basis.crud.crud_sys_dept import CrudSysDept
from apps.modules.sys.basis.models.sys_dept import SysDeptModel
from apps.modules.sys.basis.params.sys_dept import SysDeptAddParam, SysDeptEditParam
from apps.modules.sys.basis.schemas.sys_dept import SysDeptSchema
from core.common.param import ChangeStatusParam
from core.framework.auth import PreAuthorize
from core.framework.crud_async_session import AsyncGenericCRUD, crud_getter
from core.framework.decorators import transaction
from core.framework.response import SuccessResponse, ErrorResponse

dept_router = APIRouter(prefix="/dept")

@dept_router.post("/add_dept", summary="新增部门")
async def add(sys_dept_add_param: SysDeptAddParam,
              crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysDeptModel)),
              _ = Depends(PreAuthorize(permissions=["system:dept:add"]))):
    sys_dept = await crud_async_session.create(sys_dept_add_param)
    await CrudSysDept.associationDeptLeader(sys_dept.id, sys_dept_add_param.dept_leader_user_ids, crud_async_session)
    return SuccessResponse("OK")

@dept_router.put("/edit_dept", summary="编辑部门")
@transaction
async def edit(sys_dept_edit_param: SysDeptEditParam,
               crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysDeptModel)),
               _ = Depends(PreAuthorize(permissions=["system:dept:edit"]))):
    db_obj = await crud_async_session.get(sys_dept_edit_param.id)
    if not db_obj:
        return ErrorResponse("部门不存在")
    await crud_async_session.update(sys_dept_edit_param, db_obj)
    await CrudSysDept.associationDeptLeader(db_obj.id, sys_dept_edit_param.dept_leader_user_ids, crud_async_session)
    return SuccessResponse("OK")

@dept_router.delete("/{dept_id}/delete_dept", summary="删除部门")
async def delete_dept(dept_id: int,
               crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysDeptModel)),
               _ = Depends(PreAuthorize(permissions=["system:dept:delete"]))):
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
async def get_dept_all_tree(disabled_of_dept_id: Optional[int] = Query(default=None, description="部门ID，如果指定，数据ID为此值时标识为禁用，告诉前端禁用此项"), crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysDeptModel))):
    dept_all_tree = await CrudSysDept.get_dept_all_tree(disabled_of_dept_id, True, crud_async_session)
    return SuccessResponse(dept_all_tree)

@dept_router.get("/get_simple_dept_all_tree", summary="查询所有部门树不返回设置部门负责任")
async def get_simple_dept_all_tree(crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysDeptModel))):
    data_list: List[SysDeptSchema] = await CrudSysDept.get_dept_all_tree(None,False, crud_async_session)
    return SuccessResponse(data_list)
