from fastapi import APIRouter, Depends, Path
from sqlalchemy import select, exists

from apps.modules.sys.scheduler.crud.crud_job_group import fetch_job_group_list
from apps.modules.sys.scheduler.models.job_group import JobGroupModel
from apps.modules.sys.scheduler.models.job_scheduler import JobSchedulerModel
from apps.modules.sys.scheduler.params.job_group import JobGroupPageParam, JobGroupAddParam, JobGroupEditParam
from apps.modules.sys.scheduler.schemas.job_group import JobGroupSchema
from core.framework.crud_async_session import AsyncGenericCRUD, crud_getter
from core.framework.response import SuccessResponse, ErrorResponse

job_group_router = APIRouter(prefix="/job_group")

@job_group_router.post("/get_job_group_list", summary="任务组列表")
async def get_job_group_list(job_group_page_param: JobGroupPageParam,
                        crud_async_session: AsyncGenericCRUD = Depends(crud_getter(JobGroupModel))
                        ):
    page_vo = await fetch_job_group_list(job_group_page_param, crud_async_session)
    return SuccessResponse(page_vo)

@job_group_router.post("/add_job_group", summary="新增任务组")
async def add(job_group_add_param: JobGroupAddParam,
                        crud_async_session: AsyncGenericCRUD = Depends(crud_getter(JobGroupModel))
                        ):
    await crud_async_session.create(job_group_add_param)
    return SuccessResponse("OK")

@job_group_router.post("/edit_job_group", summary="编辑任务组")
async def edit(job_group_edit_param: JobGroupEditParam,
                        crud_async_session: AsyncGenericCRUD = Depends(crud_getter(JobGroupModel))
                        ):
    db_obj = await crud_async_session.get(job_group_edit_param.id)
    if not db_obj:
        return ErrorResponse("任务组不存在")
    await crud_async_session.update(job_group_edit_param, db_obj)
    return SuccessResponse("OK")

@job_group_router.get("/get_job_group_list_all", summary="获取所有任务组列表")
async def get_job_group_list_all(crud_async_session: AsyncGenericCRUD = Depends(crud_getter(JobGroupModel))):
    model_info_all = await crud_async_session.get_model_info_all(v_schema=JobGroupSchema)
    return SuccessResponse(model_info_all)

@job_group_router.post("/{job_group_id}/delete_job_group", summary="删除任务组")
async def delete_job_group(job_group_id: int = Path(description="任务组唯一ID"),
                        crud_async_session: AsyncGenericCRUD = Depends(crud_getter(JobGroupModel))
                        ):
    # 检查是否存在关联任务调度
    result = await crud_async_session.db.execute(select(exists().where(JobSchedulerModel.job_group_id == job_group_id)))
    is_job_scheduler = result.scalar()
    if is_job_scheduler :
        return ErrorResponse("存在关联任务调度，不允许删除")
    await crud_async_session.delete(job_group_id)
    return SuccessResponse("OK")
