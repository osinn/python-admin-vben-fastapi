from typing import Optional

from sqlalchemy import exists, select

from apps.modules.sys.basis.models.sys_user import SysUserModel
from apps.modules.sys.basis.params.sys_user import SysUserPageParam

from apps.modules.sys.basis.schemas.sys_user import SysUserSchema, UserRolePermissionSchema
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
        sql = [
            "select * from tbl_sys_user where is_deleted = 0"
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
        sql.append(" order by created_time desc")
        pageVo = await crud_async_session.page_select_model(" ".join(sql), sys_user_page_param.__dict__, v_schema=SysUserSchema)
        return pageVo

    @staticmethod
    async def get_sys_user_permission(user_id: int, crud_async_session: AsyncGenericCRUD):
        """
        登录获取用户权限
        :param user_id:
        :param crud_async_session:
        :return:
        """
        sql_parts = ["""
                SELECT DISTINCT
                    p.id AS permission_id,
                    p.`name` AS permission_name,
                    p.auth_code AS permission_code,
                    r.`role_code`,
                    r.`name` AS role_name,
                    r.id AS role_id 
                FROM
                    tbl_sys_role r
                    JOIN tbl_sys_user_role ur ON ur.role_id = r.id
                    LEFT JOIN tbl_sys_role_menu rp ON rp.role_id = r.id
                    LEFT JOIN tbl_sys_menu p ON rp.menu_id = p.id and p.status = 1
                    AND p.auth_code IS NOT NULL 
                    AND p.auth_code != '' 
        """]
        sql_parts.append("where r.is_deleted = 0")
        if user_id is not None:
            sql_parts.append("and ur.user_id = :user_id")
        sql = " ".join(sql_parts)

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
                    'permissions': [{'permission_code': auth_constant.ALL_PERMISSION}] if row['role_code'] == auth_constant.SUPER_ADMIN_ROLE else []
                }

            if row['permission_id']:
                if row['permission_code'] and is_admin == False:
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

    @classmethod
    async def check_unique_email(cls, email: str, id: Optional[int], crud_async_session: AsyncGenericCRUD) -> bool:
        if email is None:
            return False
        su_bq = exists().where(SysUserModel.email == email, SysUserModel.is_deleted == False)
        if id:
            su_bq = su_bq.where(SysUserModel.id != id)
        result = await crud_async_session.db.execute(select(su_bq))
        return result.scalar()

    @classmethod
    async def check_unique_staff_number(cls, staff_number: str, id: Optional[int], crud_async_session: AsyncGenericCRUD):
        if staff_number is None:
            return False
        su_bq = exists().where(SysUserModel.staff_number == staff_number, SysUserModel.is_deleted == False)
        if id:
            su_bq = su_bq.where(SysUserModel.id != id)
        result = await crud_async_session.db.execute(select(su_bq))
        return result.scalar()

    @classmethod
    async def delete_user_post_and_role_of_user_id(cls, user_id: int, crud_async_session):
        sql = "DELETE FROM tbl_sys_user_post WHERE user_id = :user_id"
        await crud_async_session.execute_sql(sql, {"user_id": user_id})
        sql = "DELETE FROM tbl_sys_user_role WHERE user_id = :user_id"
        await crud_async_session.execute_sql(sql, {"user_id": user_id})