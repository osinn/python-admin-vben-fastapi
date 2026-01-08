from apps.modules.sys.basis.params.sys_user import SysUserPageParam

from apps.modules.sys.basis.schemas.sys_user import SysUserSchema
from core.framework.crud_async_session import AsyncGenericCRUD

class CrudSysMenu:

    @staticmethod
    async def page_query_user_list(sys_user_page_param: SysUserPageParam, crud_async_session: AsyncGenericCRUD):
        """
        分页查询用户列表
        :param sys_user_page_param:
        :param crud_async_session:
        :return:
        """
        sql = (f"select * from tbl_sys_user where is_deleted = 0"
               f"{
               " and status = :status" if sys_user_page_param.status is not None else ''
               }"
               f"{
               " and sex =: sex" if sys_user_page_param.sex is not None else ''
               }"
               f"{
               " and dept_id =: dept_id" if sys_user_page_param.dept_id is not None else ''
               }"
               f"{
               " and (nickname LIKE CONCAT('%', :search_key, '%') "
               "OR account LIKE CONCAT('%', :search_key, '%') "
               "OR phone LIKE CONCAT('%', :search_key, '%') "
               "OR staff_number LIKE CONCAT('%', :search_key, '%') "
               "OR email LIKE CONCAT('%', :search_key, '%') )" if sys_user_page_param.search_key is not None else ''
               }"
               )
        pageVo = await crud_async_session.page_select_model(sql, sys_user_page_param.__dict__, v_schema=SysUserSchema)
        return pageVo