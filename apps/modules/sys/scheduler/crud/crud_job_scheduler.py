from apps.modules.sys.scheduler.params.job_scheduler import JobSchedulerPageParam
from apps.modules.sys.scheduler.schemas.job_scheduler import JobSchedulerSchema
from core.framework.crud_async_session import AsyncGenericCRUD


async def fetch_job_scheduler_list(job_scheduler_page_param: JobSchedulerPageParam,
                        crud_async_session: AsyncGenericCRUD):
    sql = [
        """
        select * from tbl_job_scheduler where is_deleted = false
        """
    ]

    if job_scheduler_page_param.search_key:
        sql.append("""
        and (
            job_id like concat('%', :search_key, '%')
            or remarks like concat('%', :search_key, '%')
            or author like concat('%', :search_key, '%')
            or executor_handler like concat('%', :search_key, '%')
            or alarm_email like concat('%', :search_key, '%')
        )
        """)
    sql.append(" order by created_time desc")
    page_vo = await crud_async_session.page_select_model("".join(sql), job_scheduler_page_param.__dict__, v_schema=JobSchedulerSchema)
    return page_vo

