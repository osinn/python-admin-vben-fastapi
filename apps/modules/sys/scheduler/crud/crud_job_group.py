from apps.modules.sys.scheduler.params.job_group import JobGroupPageParam
from apps.modules.sys.scheduler.schemas.job_group import JobGroupSchema
from core.framework.crud_async_session import AsyncGenericCRUD


async def fetch_job_group_list(job_group_page_param: JobGroupPageParam, crud_async_session: AsyncGenericCRUD):
    sql = [
        """
        select * from tbl_job_group where is_deleted = false
        """
    ]
    if job_group_page_param.group_name:
        sql.append(" and  group_name like concat('%', :group_name, '%')")
    sql.append(" order by created_time desc")
    page_vo = await crud_async_session.page_select_model("".join(sql), job_group_page_param.__dict__, v_schema=JobGroupSchema)
    return page_vo
