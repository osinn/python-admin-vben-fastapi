from fastapi import APIRouter, Depends, Path

from apps.modules.sys.scheduler.crud.crud_job_scheduler import fetch_job_scheduler_list
from apps.modules.sys.scheduler.models.job_scheduler import JobSchedulerModel
from apps.modules.sys.scheduler.params.job_scheduler import JobSchedulerPageParam, JobSchedulerAddParam
from core.framework.crud_async_session import AsyncGenericCRUD, crud_getter
from core.framework.response import SuccessResponse, ErrorResponse

job_scheduler_router = APIRouter(prefix="/job_scheduler")

@job_scheduler_router.post("/get_job_scheduler_list", summary="任务调度列表查询")
async def get_job_scheduler_list(job_scheduler_page_param: JobSchedulerPageParam,
                        crud_async_session: AsyncGenericCRUD = Depends(crud_getter(JobSchedulerModel))
                        ):
    page_vo = await fetch_job_scheduler_list(job_scheduler_page_param, crud_async_session)
    return SuccessResponse(page_vo)


@job_scheduler_router.post("/add_job_scheduler", summary="新增任务调度")
async def add_job_scheduler(job_scheduler_add_param: JobSchedulerAddParam,
                        crud_async_session: AsyncGenericCRUD = Depends(crud_getter(JobSchedulerModel))
                        ):
    await crud_async_session.create(job_scheduler_add_param)
    return SuccessResponse("OK")

@job_scheduler_router.post("/edit_job_scheduler", summary="编辑任务调度")
async def edit(job_scheduler_edit_param: JobSchedulerAddParam,
                        crud_async_session: AsyncGenericCRUD = Depends(crud_getter(JobSchedulerModel))
                        ):
    db_obj = await crud_async_session.get(job_scheduler_edit_param.id)
    if not db_obj:
        return ErrorResponse("任务调度不存在")
    await crud_async_session.update(job_scheduler_edit_param, db_obj)
    return SuccessResponse("OK")

@job_scheduler_router.post("/{job_scheduler_id}/delete_job_scheduler", summary="删除任务调度")
async def delete_job_scheduler(job_scheduler_id: int = Path(description="任务调度唯一ID"),
                        crud_async_session: AsyncGenericCRUD = Depends(crud_getter(JobSchedulerModel))
                        ):
    
    """
    移除定时任务调度
    """
    # scheduler_service = job_scheduler.get_scheduler_service()
    # scheduler_service.remove_job('add_job1')
    # 先移除定时任务调度再删除数据库数据
    await crud_async_session.delete(job_scheduler_id)
    return SuccessResponse("OK")


@job_scheduler_router.post("/{job_scheduler_id}/pause_job_scheduler", summary="暂停任务调度")
async def pause_job_scheduler(job_scheduler_id: int = Path(description="任务调度唯一ID"),
                               crud_async_session: AsyncGenericCRUD = Depends(crud_getter(JobSchedulerModel))
                               ):
    """
    从数据库中查询出调度信息，根据调度唯一标识移除调度
    :param job_scheduler_id:
    :param crud_async_session:
    :return:
    """
    # job = await crud_async_session.get(job_scheduler_id)
    # scheduler_service = job_scheduler.get_scheduler_service()
    # scheduler_service.remove_job(job.job_key)
    return SuccessResponse("OK")


@job_scheduler_router.post("/{job_scheduler_id}/resume_job_scheduler", summary="继续任务调度")
async def resume_job_scheduler(job_scheduler_id: int = Path(description="任务调度唯一ID"),
                               crud_async_session: AsyncGenericCRUD = Depends(crud_getter(JobSchedulerModel))
                               ):
    """
    从数据库中查询出调度信息，重新添加到任务调度中
    :param job_scheduler_id:
    :param crud_async_session:
    :return:
    """
    # job = await crud_async_session.get(job_scheduler_id)
    # scheduler_service = job_scheduler.get_scheduler_service()
    # # 3秒执行一次定时任务，调用 sync_job 函数
    # scheduler_service.add_job(sync_job, "interval", seconds=3, id="add_job1")

    return SuccessResponse("OK")
