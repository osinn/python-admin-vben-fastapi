from apps.modules.sys.basis.params.sys_post import SysPostQueryParam
from apps.modules.sys.basis.schemas.sys_post import SysPostSchema

from core.framework.crud_async_session import AsyncGenericCRUD

class CrudSysPost:

    @staticmethod
    async def page_query_post_list(sys_post_query_param: SysPostQueryParam, crud_async_session: AsyncGenericCRUD):
        """
        分页查询岗位列表
        :param sys_post_query_param:
        :param crud_async_session:
        :return:
        """
        sql = [
            "select * from tbl_sys_post where is_deleted = false"
        ]
        if sys_post_query_param.search_key is not None:
            sql.append("""
            and (
                   name LIKE CONCAT('%', :search_key, '%') 
                   OR post_code LIKE CONCAT('%', :search_key, '%')
               )
            """)
        if sys_post_query_param.status is not None:
            sql.append('and status = :status')
        page_vo = await crud_async_session.page_select_model(" ".join(sql), sys_post_query_param.__dict__, v_schema=SysPostSchema)
        return page_vo

    @classmethod
    async def get_dept_post_list_by_dept_id(cls, dept_post_query_param, crud_async_session):
        sql = [
            """
                  SELECT
                    distinct p.*,
                    IF(dp.id,1, 0) as checked
                  FROM
                    tbl_sys_post p
                      LEFT JOIN tbl_sys_dept_post dp ON dp.post_id = p.id
                      and dp.dept_id = :dept_id
                  where is_deleted = 0
            """
        ]
        if dept_post_query_param.checked is not None:
            if dept_post_query_param.checked:
                sql.append('and dp.dept_id is not null')
            else:
                sql.append('and dp.dept_id is null')
        if dept_post_query_param.status is not None:
            sql.append(' and p.status = :status')
        sql.append('order by p.sort desc, p.id desc')
        page_vo = await crud_async_session.page_select_model(" ".join(sql), dept_post_query_param.__dict__, v_schema=SysPostSchema)
        return page_vo