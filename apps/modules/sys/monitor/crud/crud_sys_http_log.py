from apps.modules.sys.monitor.models.sys_http_log import SysHttpLogModel
from apps.modules.sys.monitor.params.sys_http_log import SysLoginLogPageParam
from apps.modules.sys.monitor.schemas.sys_http_log import SysHttpLogSchema
from core.framework.crud_async_session import AsyncGenericCRUD


class CrudSysHttpLog:

    @classmethod
    async def get_login_log_info_list(cls, sys_login_log_page_param: SysLoginLogPageParam, crud_async_session: AsyncGenericCRUD):
        """
        登录日志查询
        """
        sql = [
            """
            select * from tbl_sys_http_log where 1 = 1
            """
        ]

        if sys_login_log_page_param.search_key:
            sql.append(
                """
                and (
                    nickname LIKE CONCAT('%', :search_key, '%')
                    OR account LIKE CONCAT('%', :search_key, '%') 
                 )
                """
            )

        if sys_login_log_page_param.status is not None:
            sql.append("and status = :status")

        if sys_login_log_page_param.log_type is not None:
            sql.append("and log_type = :log_type")

        if sys_login_log_page_param.start_created_time and sys_login_log_page_param.end_created_time:
            sql.append("and created_time between :start_created_time and :end_created_time")
        sql.append(" order by created_time desc")
        page_vo = await crud_async_session.page_select_model(" ".join(sql), sys_login_log_page_param.__dict__, v_schema=SysHttpLogSchema)
        return page_vo

    @classmethod
    async def create_login_log(cls, sys_http_log: SysHttpLogModel, crud_async_session: AsyncGenericCRUD):
        """
        创建登录日志
        """
        crud_async_session.db.add(sys_http_log)
        await crud_async_session.db.commit()