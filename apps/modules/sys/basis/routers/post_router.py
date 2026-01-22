from certifi import where
from fastapi import APIRouter, Depends, Path, Request
from sqlalchemy import delete

from apps.modules.sys.basis.crud.crud_sys_post import CrudSysPost
from apps.modules.sys.basis.crud.crud_sys_user import CrudSysUser
from apps.modules.sys.basis.models.sys_dept_post import SysDeptPostModel
from apps.modules.sys.basis.models.sys_post import SysPostModel
from apps.modules.sys.basis.params.sys_post import SysPostQueryParam, SysPostAddParam, SysPostEditParam, \
    DeptPostQueryParam, DeptPostParam
from apps.modules.sys.basis.schemas.sys_post import SysPostSchema
from core.common.param import ChangeStatusParam
from core.framework.auth import PreAuthorize
from core.framework.crud_async_session import crud_getter, AsyncGenericCRUD
from core.framework.response import SuccessResponse, ErrorResponse

post_router = APIRouter(prefix="/post")


@post_router.post("/get_post_list", summary="获取岗位列表")
async def get_post_list(sys_post_query_param: SysPostQueryParam,
                        crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysPostModel))):
    page_vo = await CrudSysPost.page_query_post_list(sys_post_query_param, crud_async_session)
    await crud_async_session.fill_base_user_info(page_vo.items)
    return SuccessResponse(page_vo)


@post_router.post("/add_post", summary="新增岗位")
async def add(sys_post_add_param: SysPostAddParam,
              crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysPostModel)),
              _=Depends(PreAuthorize(permissions=["system:post:add"]))
              ):
    await crud_async_session.create(sys_post_add_param)
    return SuccessResponse("OK")


@post_router.put("/edit_post", summary="编辑岗位")
async def edit(sys_post_edit_param: SysPostEditParam,
               crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysPostModel)),
               _=Depends(PreAuthorize(permissions=["system:post:edit"]))
               ):
    db_obj = await crud_async_session.get(sys_post_edit_param.id)
    if not db_obj:
        return ErrorResponse("岗位不存在")
    await crud_async_session.update(sys_post_edit_param, db_obj)
    return SuccessResponse("OK")


@post_router.delete("/{post_id}/delete_post", summary="删除岗位")
async def delete_post(post_id: int = Path(description="岗位唯一ID"),
                      crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysPostModel)),
                      _=Depends(PreAuthorize(permissions=["system:post:delete"]))
                      ):
    result = await crud_async_session.delete(post_id)
    if not result:
        return ErrorResponse("删除失败")
    return SuccessResponse("OK")


@post_router.put("/sys_post_change_status", summary="修改岗位状态")
async def sys_user_reset(change_status_param: ChangeStatusParam,
                         crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysPostModel)),
                         _=Depends(PreAuthorize(permissions=["system:post:changeStatus"]))
                         ):
    result: bool = await crud_async_session.change_status(change_status_param.id, change_status_param.status)
    if not result:
        return ErrorResponse("状态更新失败")
    return SuccessResponse("OK")


@post_router.get("/get_post_list_all", summary="获取全部岗位列表")
async def get_post_list(crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysPostModel))):
    model_info_all = await crud_async_session.get_model_info_all(v_schema=SysPostSchema)
    return SuccessResponse(model_info_all)


@post_router.post("/get_dept_post_list_by_dept_id", summary="获取部门岗位列表")
async def get_dept_post_list_by_dept_id(dept_post_query_param: DeptPostQueryParam,
                                        crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysPostModel))):
    page_vo = await CrudSysPost.get_dept_post_list_by_dept_id(dept_post_query_param, crud_async_session)
    return SuccessResponse(page_vo)


@post_router.post("/add_dept_post", summary="关联部门岗位")
async def add_dept_post(request: Request, dept_post_add_param: DeptPostParam,
                        crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysDeptPostModel))):
    sys_dept_post_models = []
    for post_id in dept_post_add_param.post_ids:
        sys_dept_post_model = SysDeptPostModel()
        sys_dept_post_model.dept_id = dept_post_add_param.dept_id
        sys_dept_post_model.post_id = post_id
        user = getattr(request.state, "user", None)
        if user and user.get("id", None) is not None:
            sys_dept_post_model.created_by = user.get("id", None)
        sys_dept_post_models.append(sys_dept_post_model)
    crud_async_session.db.add_all(sys_dept_post_models)
    await crud_async_session.db.flush()
    return SuccessResponse()


@post_router.put("/delete_dept_post", summary="移除关联部门岗位")
async def add_dept_post(dept_post_add_param: DeptPostParam,
                        crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysDeptPostModel))):
    stmt = delete(SysDeptPostModel).where(SysDeptPostModel.post_id.in_(dept_post_add_param.post_ids),
                                          SysDeptPostModel.dept_id == dept_post_add_param.dept_id)
    await crud_async_session.db.execute(stmt)
    return SuccessResponse()
