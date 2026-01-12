from sqlalchemy.sql import roles

from apps.modules.sys.basis.params.sys_user import SysUserPageParam

from apps.modules.sys.basis.schemas.sys_user import SysUserSchema, UserRolePermissionSchema, AuthPermissionSchema
from core.constants import auth_constant
from core.framework.crud_async_session import AsyncGenericCRUD

class CrudSysUser:

    @staticmethod
    async def page_query_user_list(sys_user_page_param: SysUserPageParam, crud_async_session: AsyncGenericCRUD):
        """
        分页查询用户列表
        :param sys_user_page_param:
        :param crud_async_session:
        :return:
        """
        # sql = (f"select * from tbl_sys_user where is_deleted = false"
        #        f"{
        #        " and status = :status" if sys_user_page_param.status is not None else ''
        #        }"
        #        f"{
        #        " and sex = :sex" if sys_user_page_param.sex is not None else ''
        #        }"
        #        f"{
        #        " and dept_id = :dept_id" if sys_user_page_param.dept_id is not None else ''
        #        }"
        #        f"{
        #        " and (nickname LIKE CONCAT('%', :search_key, '%') "
        #        "OR account LIKE CONCAT('%', :search_key, '%') "
        #        "OR phone LIKE CONCAT('%', :search_key, '%') "
        #        "OR staff_number LIKE CONCAT('%', :search_key, '%') "
        #        "OR email LIKE CONCAT('%', :search_key, '%') )" if sys_user_page_param.search_key is not None else ''
        #        }"
        #        )
        sql = [
            "select * from tbl_sys_user where is_deleted = false"
        ]
        if sys_user_page_param.status is not None:
            sql.append(" and status = :status")
        if sys_user_page_param.sex is not None:
            sql.append(" and sex = :sex")
        if sys_user_page_param.dept_id is not None:
            sql.append(" and dept_id = :dept_id")
        if sys_user_page_param.search_key is not None:
            sql.append(
                """
                and (
                    nickname LIKE CONCAT('%', :search_key, '%')
                    OR account LIKE CONCAT('%', :search_key, '%') 
                    OR phone LIKE CONCAT('%', :search_key, '%') 
                    OR staff_number LIKE CONCAT('%', :search_key, '%') 
                    OR email LIKE CONCAT('%', :search_key, '%') 
                 )
                """
            )
        pageVo = await crud_async_session.page_select_model("".join(sql), sys_user_page_param.__dict__, v_schema=SysUserSchema)
        return pageVo

    @staticmethod
    async def get_sys_user_permission(user_id: int, crud_async_session: AsyncGenericCRUD):
        sql_parts = ["""
              SELECT
                DISTINCT p.id as permission_id,
                         p.`name` as permission_name,
                         p.auth_code as permission_code,
                         r.`role_code`,
                         r.`name` as role_name,
                         r.id as role_id
              FROM
                tbl_sys_menu p
                  JOIN tbl_sys_role_menu rp ON rp.menu_id = p.id
                  JOIN tbl_sys_role r ON rp.role_id = r.id
                  JOIN tbl_sys_user_role ur ON ur.role_id = r.id
                  AND p.auth_code is not null and p.auth_code != ''
        """]
        if user_id is not None:
            sql_parts.append(" AND ur.user_id = :user_id")
        sql = "".join(sql_parts)

        permissions = await crud_async_session.list_model(sql, {"user_id": user_id})
        is_admin = any(p["role_code"] == auth_constant.SUPER_ADMIN_ROLE for p in permissions)

        # 分组处理
        roles = {}
        for row in permissions:
            role_id = row['role_id']

            if role_id not in roles:
                roles[role_id] = {
                    'role_id': role_id,
                    'role_code': row['role_code'],
                    'role_name': row['role_name'],
                    'permissions': []
                }

            if row['permission_id']:
                """
                如果存在管理员角色，只将管理员角色设置成全部权限，普通角色不赋值权限编码
                """
                if is_admin == True and row.get("role_code") == auth_constant.SUPER_ADMIN_ROLE and not roles[role_id]['permissions']:
                    # 如果是管理员角色，没有设置过权限编码，则权限编码设置为全部权限编码
                    roles[role_id]['permissions'].append({
                        'permission_code': auth_constant.ALL_PERMISSION,
                    })
                elif is_admin == False and row.get("role_code") != auth_constant.SUPER_ADMIN_ROLE:
                    # 如果不是管理员，则根据角色拥有的权限分组
                    roles[role_id]['permissions'].append({
                        'permission_id': row['permission_id'],
                        'permission_code': row['permission_code'],
                        'permission_name': row['permission_name']
                    })

        # 转换为Pydantic模型
        return [
                UserRolePermissionSchema(**role_data)
                for role_data in roles.values()
            ]
