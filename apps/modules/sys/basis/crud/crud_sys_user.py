from collections import defaultdict
from typing import Optional, List

from sqlalchemy import exists, select

from apps.modules.sys.basis.models.sys_user import SysUserModel
from apps.modules.sys.basis.params.sys_user import SysUserPageParam

from apps.modules.sys.basis.schemas.sys_user import SysUserSchema, UserRolePermissionSchema, AuthPermissionSchema
from core.constants import auth_constant
from core.framework.common_schemas import BaseSchema
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
                elif row['permission_code'] and is_admin == False and row.get("role_code") != auth_constant.SUPER_ADMIN_ROLE:
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

    @staticmethod
    async def fill_base_user_info(base_user_list: List[BaseSchema], crud_async_session: AsyncGenericCRUD) -> None:
        if len(base_user_list) == 0:
            return
        user_ids = set()
        for user in base_user_list:
            if user.created_by:
                user_ids.add(user.created_by)
            if user.updated_by:
                user_ids.add(user.updated_by)

        if len(user_ids) != 0:
            # in 查询集合转元数组
            user_data = await crud_async_session.execute_sql("select id, nickname from tbl_sys_user where is_deleted = 0 and id in :user_ids", {"user_ids": tuple(user_ids)},fetch_data=True)
            user_name_map = {item['id']: item['nickname'] for item in user_data}
            for user in base_user_list:

                if user.created_by:
                    user_name = user_name_map.get(user.created_by, None)
                    user.created_by_name = user_name
                if user.updated_by:
                    user_name = user_name_map.get(user.updated_by, None)
                    user.created_by_name = user_name
    @staticmethod
    async def fill_user_data(user_data: List[SysUserSchema], crud_async_session: AsyncGenericCRUD) -> None:
        if len(user_data) == 0:
            return None
        dept_ids = set()
        user_ids = set()
        for user in user_data:
            user_ids.add(user.id)
            if user.dept_id:
                dept_ids.add(user.dept_id)

        dept_name_map = {}

        if len(dept_ids) != 0:
            # in 查询集合转元数组
            dept_data = await crud_async_session.execute_sql("select id, name from tbl_sys_dept where is_deleted = 0 and id in :dept_ids", {"dept_ids": tuple(dept_ids)},fetch_data=True)
            dept_name_map = {item['id']: item['name'] for item in dept_data}

        role_sql = """
            SELECT
              r.id,
              r.name,
              ur.user_id
            FROM
              tbl_sys_role r
                JOIN tbl_sys_user_role ur ON ur.role_id = r.id
                AND ur.user_id IN :user_ids
            where r.is_deleted = 0
        """

        post_sql = """
          SELECT
            p.id,
            p.name, 
           up.user_id
          FROM
            tbl_sys_post p
              JOIN tbl_sys_user_post up ON up.post_id = p.id
              AND up.user_id IN :user_ids
          where p.is_deleted = 0
        """

        role_data = await crud_async_session.execute_sql(role_sql,{"user_ids": tuple(user_ids)}, fetch_data=True)
        post_data = await crud_async_session.execute_sql(post_sql,{"user_ids": tuple(user_ids)}, fetch_data=True)

        role_map = defaultdict(list)
        for entity in role_data:
            user_id = entity["user_id"]
            role_map[user_id].append(entity)

        post_map = defaultdict(list)
        for entity in post_data:
            user_id = entity["user_id"]
            post_map[user_id].append(entity)

        for user in user_data:
            roles = role_map.get(user.id, [])
            posts = post_map.get(user.id, [])
            if user.dept_id:
                dept_name = dept_name_map.get(user.dept_id, None)
                user.dept_name = dept_name
            role_ids = []
            role_names = []
            for role in roles:
                role_ids.append(role["id"])
                role_names.append(role["name"])

            post_ids = []
            post_names = []
            for post in posts:
                post_ids.append(post["id"])
                post_names.append(post["name"])

            user.role_ids = role_ids
            user.role_names = ",".join(role_names)
            user.post_ids = post_ids
            user.post_names = ",".join(post_names)
