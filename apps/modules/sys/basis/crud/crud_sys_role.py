from apps.modules.sys.basis.params.sys_role import SysRolePageParam
from apps.modules.sys.basis.schemas.sys_role import SysRoleSchema

from core.framework.crud_async_session import AsyncGenericCRUD

class CrudSysRole:

    @staticmethod
    async def page_query_role_list(sys_role_page_param: SysRolePageParam, crud_async_session: AsyncGenericCRUD):
        """
        分页查询用户列表
        :param sys_user_page_param:
        :param crud_async_session:
        :return:
        """
        # sql = (f"select * from tbl_sys_role where is_deleted = false"
        #        f"{
        #        " and status = :status" if sys_role_page_param.status is not None else ''
        #        }"
        #        f"{
        #        " and ("
        #            "name LIKE CONCAT('%', :search_key, '%') "
        #            "OR role_code LIKE CONCAT('%', :search_key, '%') "
        #        ")" if sys_role_page_param.search_key is not None else ''
        #        }"
        #        )
        sql = [
            "select * from tbl_sys_role where is_deleted = false"
        ]
        if sys_role_page_param.search_key is not None:
            sql.append("""
            and (
                   name LIKE CONCAT('%', :search_key, '%') 
                   OR role_code LIKE CONCAT('%', :search_key, '%')
               )
            """)
        pageVo = await crud_async_session.page_select_model("".join(sql), sys_role_page_param.__dict__, v_schema=SysRoleSchema)
        return pageVo