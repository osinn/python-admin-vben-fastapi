from fastapi import APIRouter, Depends, Path
from sqlalchemy import select, exists

from apps.modules.sys.scheduler.crud.crud_job_scheduler import fetch_job_scheduler_list
from apps.modules.sys.scheduler.models.job_scheduler import JobSchedulerModel
from apps.modules.sys.scheduler.params.job_scheduler import JobSchedulerPageParam, JobSchedulerAddParam
from core.framework.auth import PreAuthorize
from core.framework.crud_async_session import AsyncGenericCRUD, crud_getter
from core.framework.response import SuccessResponse, ErrorResponse
from core.framework.scheduler_tools import job_scheduler

job_scheduler_router = APIRouter(prefix="/job_scheduler")

@job_scheduler_router.post("/get_job_scheduler_list", summary="任务调度列表查询")
async def get_job_scheduler_list(job_scheduler_page_param: JobSchedulerPageParam,
                        crud_async_session: AsyncGenericCRUD = Depends(crud_getter(JobSchedulerModel))
                        ):
    page_vo = await fetch_job_scheduler_list(job_scheduler_page_param, crud_async_session)
    return SuccessResponse(page_vo)


@job_scheduler_router.get("/get_job_scheduler_all", summary="任务调度列表查询")
async def get_job_scheduler_all():
    jobs = job_scheduler.get_scheduler_service().get_jobs()
    return SuccessResponse("OK")


@job_scheduler_router.post("/add_job_scheduler", summary="新增任务调度")
async def add_job_scheduler(job_scheduler_add_param: JobSchedulerAddParam,
                        crud_async_session: AsyncGenericCRUD = Depends(crud_getter(JobSchedulerModel)),
                        _ = Depends(PreAuthorize(permissions=["scheduler:job:add"]))
                        ):
    result = await crud_async_session.db.execute(select(exists().where(JobSchedulerModel.job_id == job_scheduler_add_param.job_id)))
    is_job_scheduler = result.scalar()
    if is_job_scheduler :
        return ErrorResponse("任务唯一标识已存在，不允许重复")

    await crud_async_session.create(job_scheduler_add_param)
    return SuccessResponse("OK")

@job_scheduler_router.post("/edit_job_scheduler", summary="编辑任务调度")
async def edit(job_scheduler_edit_param: JobSchedulerAddParam,
                        crud_async_session: AsyncGenericCRUD = Depends(crud_getter(JobSchedulerModel)),
                        _ = Depends(PreAuthorize(permissions=["scheduler:job:edit"]))
                        ):
    db_obj = await crud_async_session.get(job_scheduler_edit_param.id)
    if not db_obj:
        return ErrorResponse("任务调度不存在")
    result = await crud_async_session.db.execute(select(exists().where(
        JobSchedulerModel.job_id == job_scheduler_edit_param.job_id,
        JobSchedulerModel.id != job_scheduler_edit_param.id
    )))
    is_job_scheduler = result.scalar()
    if is_job_scheduler :
        return ErrorResponse("任务唯一标识已存在，不允许重复")
    job = job_scheduler.get_scheduler_service().get_job(db_obj.job_id)
    if job is None:
        if job_scheduler_edit_param.job_id != db_obj.job_id:
            job_scheduler.get_scheduler_service().remove_job( db_obj.job_id)

    await crud_async_session.update(job_scheduler_edit_param, db_obj)
    return SuccessResponse("OK")

@job_scheduler_router.delete("/{job_scheduler_id}/delete_job_scheduler", summary="删除任务调度")
async def delete_job_scheduler(job_scheduler_id: int = Path(description="任务调度唯一ID"),
                        crud_async_session: AsyncGenericCRUD = Depends(crud_getter(JobSchedulerModel)),
                        _ = Depends(PreAuthorize(permissions=["scheduler:job:delete"]))
                        ):
    db_obj = await crud_async_session.get(job_scheduler_id)
    if not db_obj:
        return ErrorResponse("任务调度不存在")
    # 先移除定时任务调度再删除数据库数据
    await crud_async_session.delete(job_scheduler_id)
    """
    移除定时任务调度
    """
    scheduler_service = job_scheduler.get_scheduler_service()
    scheduler_service.pause(db_obj.task_id)
    scheduler_service.remove_job(db_obj.task_id)
    return SuccessResponse("OK")

@job_scheduler_router.put("/{job_scheduler_id}/pause_job_scheduler", summary="暂停任务调度")
async def pause_job_scheduler(job_scheduler_id: int = Path(description="任务调度唯一ID"),
                               crud_async_session: AsyncGenericCRUD = Depends(crud_getter(JobSchedulerModel)),
                               _ = Depends(PreAuthorize(permissions=["scheduler:job:pause"]))
                               ):
    db_obj = await crud_async_session.get(job_scheduler_id)
    if not db_obj:
        return ErrorResponse("任务调度不存在")
    db_obj.job_status = 2
    job_scheduler.get_scheduler_service().pause_job(db_obj.job_id)
    return SuccessResponse("OK")

@job_scheduler_router.put("/{job_scheduler_id}/resume_job_scheduler", summary="继续任务调度")
async def resume_job_scheduler(job_scheduler_id: int = Path(description="任务调度唯一ID"),
                               crud_async_session: AsyncGenericCRUD = Depends(crud_getter(JobSchedulerModel)),
                                _ = Depends(PreAuthorize(permissions=["scheduler:job:resume"]))
                               ):
    db_obj = await crud_async_session.get(job_scheduler_id)
    if not db_obj:
        return ErrorResponse("任务调度不存在")
    db_obj.job_status = 1
    job_scheduler.get_scheduler_service().resume_job(db_obj.job_id)
    return SuccessResponse("OK")