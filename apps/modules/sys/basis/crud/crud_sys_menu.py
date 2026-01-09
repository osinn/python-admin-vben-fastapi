from typing import List

from sqlalchemy import select, exists

from apps.modules.sys.basis.models.sys_menu import SysMenuModel
from apps.modules.sys.basis.models.sys_role import SysRoleModel
from apps.modules.sys.basis.schemas.sys_menu import RouteItemSchema, RouteMetaSchema

from core.constants.auth_constant import SUPER_ADMIN_ROLE
from core.framework.crud_async_session import AsyncGenericCRUD
from core.utils.JSONUtils import JSONUtils


class CrudSysMenu:

    @staticmethod
    async def get_assignment_permission_ids_by_role_id(role_id: int, crud_async_session: AsyncGenericCRUD):
        """
        查询分配给角色的权限菜单ID
        :param role_id: 角色ID
        :param crud_async_session:
        :return:
        """
        result = await crud_async_session.db.execute(select(exists().where(SysRoleModel.id == role_id, SysRoleModel.role_code == SUPER_ADMIN_ROLE)))
        is_admin = result.scalar()
        # 是不是管理员
        if is_admin:
            result = await crud_async_session.db.execute(
                select(crud_async_session.model_class.id).where(
                    crud_async_session.model_class.is_deleted == 0,
                    crud_async_session.model_class.status == 0
                )
            )
            rows = result.scalars().all()
            return rows
        else:
            sql = [
                """
                    SELECT
                      m.id
                    FROM
                      tbl_sys_menu m
                        JOIN tbl_sys_role_menu rm ON rm.menu_id = m.id AND rm.role_id and rm.role_id = :role_id
                """
            ]
            rows = await crud_async_session.list_model("".join(sql), {"role_id": role_id})
            return [item["id"] for item in rows]
    @staticmethod
    async def get_menu_tree_list_all(crud_async_session: AsyncGenericCRUD):
        """
          查询 model 所有非删除数据
          :param v_schema 指定序列化，如果指定，则序列化后返回 v_schema 对象集合，否则返回 model 对象集合
          :return:
          """
        result = await crud_async_session.db.execute(
            select(crud_async_session.model_class).where(crud_async_session.model_class.is_deleted == 0)
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

            # 递归构建 children
            children = [
                _convert_to_vo(child)
                for child in children_map[sys_menu.id]
            ]

            # 构造 VO（假设 SysMenuModel 字段与 RouteItemSchema 一致）
            return RouteItemSchema(
                id=sys_menu.id,
                parent_id=sys_menu.parent_id,
                name=sys_menu.name,
                meta=meta_obj,
                children=children
            )

        # 获取根节点（parent_id == 0）
        root_nodes = children_map[0]
        return [_convert_to_vo(menu) for menu in root_nodes]