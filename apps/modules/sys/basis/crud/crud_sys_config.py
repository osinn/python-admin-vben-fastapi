from apps.modules.sys.basis.params.sys_config import SysConfigPageParam
from apps.modules.sys.basis.schemas.sys_config import SysConfigSchema
from core.framework.crud_async_session import AsyncGenericCRUD

async def get_page_config_list(sys_config_page_param: SysConfigPageParam,
                    crud_async_session: AsyncGenericCRUD):
    sql = [
        """
        select * from tbl_sys_config where is_deleted = false
        """
    ]
    if sys_config_page_param.search_key:
        sql.append(
            """
                and (
                config_group_name like concat('%', :search_key, '%')
                or config_name like concat('%', :search_key, '%')
                or config_key like concat('%', :search_key, '%')
                or config_value = :search_key
              )
            """
        )
    if sys_config_page_param.is_default is not None:
        sql.append(" and is_default = :is_default")
    if sys_config_page_param.status is not None:
        sql.append(" and status = :status")
    if sys_config_page_param.start_created_time and sys_config_page_param.end_created_time:
        sql.append(" and created_time between :start_created_time and :end_created_time")
    sql.append(" order by created_time desc")
    page_vo = await crud_async_session.page_select_model(" ".join(sql), sys_config_page_param.__dict__, v_schema=SysConfigSchema)
    return page_vo
