from typing import List, cast

from sqlalchemy import select, exists, distinct, and_

from apps.modules.sys.basis.models.sys_menu import SysMenuModel
from apps.modules.sys.basis.models.sys_role import SysRoleModel
from apps.modules.sys.basis.schemas.sys_menu import RouteItemSchema, RouteMetaSchema, SysMenuSchema

from core.constants.auth_constant import SUPER_ADMIN_ROLE
from core.framework.crud_async_session import AsyncGenericCRUD
from core.utils.JSONUtils import JSONUtils
from core.utils.ModelUtils import ModelUtils


class CrudSysMenu:

    @staticmethod
    async def get_assignment_permission_ids_by_role_id(role_id: int, crud_async_session: AsyncGenericCRUD) -> List[int]:
        """
        查询分配给角色的权限菜单ID
        :param role_id: 角色ID
        :param crud_async_session:
        :return:
        """
        # 检查是否存在管理员
        result = await crud_async_session.db.execute(
            select(exists().where(SysRoleModel.id == role_id, SysRoleModel.role_code == SUPER_ADMIN_ROLE)))
        is_admin = result.scalar()
        # 是不是管理员
        if is_admin:
            result = await crud_async_session.db.execute(
                select(crud_async_session.model_class.id).where(
                    crud_async_session.model_class.is_deleted == False,
                    crud_async_session.model_class.status == 1
                )
            )
            rows = result.scalars().all()
            return rows
        else:
            sql = [
                """
                SELECT m.id
                FROM tbl_sys_menu m
                         JOIN tbl_sys_role_menu rm ON rm.menu_id = m.id AND rm.role_id and m.is_deleted = 0 and rm.role_id = :role_id
                """
            ]
            rows = await crud_async_session.list_model(" ".join(sql), {"role_id": role_id})
            return [item["id"] for item in rows]

    @staticmethod
    async def get_menu_tree_list_all(crud_async_session: AsyncGenericCRUD, params: dict = None) -> List[RouteItemSchema]:
        """
          查询 model 所有非删除数据
          :param v_schema 指定序列化，如果指定，则序列化后返回 v_schema 对象集合，否则返回 model 对象集合
          :return:
          """
        stmt = select(crud_async_session.model_class).where(crud_async_session.model_class.is_deleted == False)
        if params:
            filter_conditions = []
            for key, value in params.items():
                # if isinstance(value, str):
                #     condition = f"{key} == '{value}'"
                # else:
                #     condition = f"{key} == {value}"
                if value:
                    column = getattr(crud_async_session.model_class, key)
                    filter_conditions.append(column == value)
            if len(filter_conditions) > 0:
                stmt = stmt.where(and_(*filter_conditions))
        result = await crud_async_session.db.execute(
            stmt
        )
        rows = result.scalars().all()
        route_item = CrudSysMenu.__build_route_item_tree(list(rows))
        return route_item

    @staticmethod
    def __build_route_item_tree(sys_menu_list: List[SysMenuModel]) -> List[RouteItemSchema]:
        from collections import defaultdict

        children_map = defaultdict(list)
        for menu in sys_menu_list:
            children_map[menu.parent_id].append(menu)

        # 对每个分组排序
        for parent_id in children_map:
            children_map[parent_id].sort(key=lambda x: x.sort)

        def _convert_to_vo(sys_menu: SysMenuModel) -> RouteItemSchema:
            # 解析 meta
            meta_obj = RouteMetaSchema()
            if sys_menu.meta:
                try:
                    meta_data = JSONUtils.loads(sys_menu.meta) if isinstance(sys_menu.meta, str) else sys_menu.meta
                    meta_obj = RouteMetaSchema(**meta_data)
                except Exception:
                    pass

            children = [
                _convert_to_vo(child)
                for child in children_map[sys_menu.id]
            ]

            return RouteItemSchema(
                id=sys_menu.id,
                parent_id=sys_menu.parent_id,
                name=sys_menu.name,
                meta=meta_obj,
                path=sys_menu.path,
                redirect=sys_menu.redirect,
                component=sys_menu.component,
                status=sys_menu.status,
                type=sys_menu.type,
                auth_code=sys_menu.auth_code,
                children=children
            )

        # 获取根节点（parent_id == 0）
        root_nodes = children_map[0]
        return [_convert_to_vo(menu) for menu in root_nodes]

    @classmethod
    async def get_route_menu_list(cls, user_id: int, is_admin: bool, crud_async_session: AsyncGenericCRUD) -> List[
        RouteItemSchema]:
        menu_types = ["catalog", "menu", "embedded", "link"]
        if is_admin:
            result = await crud_async_session.db.execute(
                select(crud_async_session.model_class).where(
                    crud_async_session.model_class.is_deleted == False,
                    crud_async_session.model_class.status == 1,
                    crud_async_session.model_class.type.in_(menu_types)
                )
            )
            data_list = result.scalars().all()
        else:
            sql = [
                """
                SELECT distinct m.*
                FROM tbl_sys_menu m
                         JOIN tbl_sys_role_menu rm ON rm.menu_id = m.id
                         JOIN tbl_sys_role sr on sr.id = rm.role_id
                         JOIN tbl_sys_user_role sur on sur.role_id = sr.id
                    where m.is_deleted = 0
                    AND sur.user_id = :user_id
                    AND m.status = :status
                    AND m.type in :type
                """
            ]
            rows = await crud_async_session.list_model(" ".join(sql),
                                                       {"user_id": user_id, "status": 1, "type": tuple(menu_types)})
            data_list = []
            for item in rows:
                sys_menu_model = SysMenuModel()
                ModelUtils.dict_instance_attr(item, sys_menu_model)
                data_list.append(sys_menu_model)
        route_item = CrudSysMenu.__build_route_item_tree(data_list)
        return route_item

    @classmethod
    async def get_route_menu_codes(cls, user_id: int, is_admin: bool, crud_async_session: AsyncGenericCRUD) -> List[
        str]:
        if is_admin:
            result = await crud_async_session.db.execute(
                # 去重
                select(distinct(crud_async_session.model_class.auth_code)).where(
                    crud_async_session.model_class.is_deleted == False,
                    crud_async_session.model_class.status == 1,
                    crud_async_session.model_class.auth_code.isnot(None),
                    crud_async_session.model_class.auth_code != ""
                )
            )
            return cast(List[str], result.scalars().all())
        else:
            sql = [
                """
                SELECT distinct m.auth_code
                FROM tbl_sys_menu m
                         JOIN tbl_sys_role_menu rm ON rm.menu_id = m.id
                         JOIN tbl_sys_role sr on sr.id = rm.role_id
                         JOIN tbl_sys_user_role sur on sur.role_id = sr.id
                    where m.is_deleted = 0
                    AND sur.user_id = :user_id
                    AND m.status = :status
                    AND (m.auth_code is not null and m.auth_code != '')
                """
            ]
            rows = await crud_async_session.list_model(" ".join(sql),
                                                       {"user_id": user_id, "status": 1})
            return [row["auth_code"] for row in rows]
