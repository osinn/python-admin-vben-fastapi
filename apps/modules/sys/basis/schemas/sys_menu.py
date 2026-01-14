import re

from core.framework.common_schemas import BaseModelSchema
from typing import List, Optional
from pydantic import Field, ConfigDict

from core.utils.str_utils import snake_to_camel


class SysMenuSchema(BaseModelSchema):
    type: Optional[str] = Field(default=None, description="菜单类型 dir目录；menu菜单；button按钮")
    name: Optional[str] = Field(default=None, description="菜单名称")
    parent_id: Optional[int] = Field(default=None, description="上级菜单")
    path: Optional[str] = Field(default=None, description="路由地址")
    redirect: Optional[str] = Field(default=None)
    component: Optional[str] = Field(default=None, description="组件路径")
    status: Optional[bool] = Field(default=None, description="状态 0-正常；1-停用")
    auth_code: Optional[str] = Field(default=None, description="权限标识")
    sort: Optional[int] = Field(default=None, description="排序")
    remarks: Optional[str] = Field(default=None, description="备注")
    meta: Optional[str] = Field(default=None)

class RouteItemSchema(BaseModelSchema):
    id: Optional[int] = Field(default=None, description="菜单ID")
    parent_id: Optional[int] = Field(default=None, description="上级菜单")
    path: Optional[str] = Field(default=None, description="路由地址")
    redirect: Optional[str] = Field(default=None)
    component: Optional[str] = Field(default=None, description="组件路径")
    meta: Optional["RouteMetaSchema"] = Field(default=None)
    name: Optional[str] = Field(default=None, description="菜单名称")
    status: Optional[bool] = Field(default=None, description="状态 0-正常；1-停用")
    type: Optional[str] = Field(default=None, description="菜单类型 dir目录；menu菜单；button按钮")
    auth_code: Optional[str] = Field(default=None, description="权限标识")
    children: Optional[List["RouteItemSchema"]] = Field(default=[], description="子菜单")

    model_config = ConfigDict(
        # 返回浏览器序列化时下划线转驼峰命名 vhen 框架属性名称驼峰命名
        alias_generator=snake_to_camel,
        populate_by_name=True,
        from_attributes=True,
        extra="allow"
    )

class RouteMetaSchema(BaseModelSchema):
    active_icon: Optional[str] = Field(default=None, description="激活图标（菜单）")
    active_path: Optional[str] = Field(default=None, description="当前激活的菜单，有时候不想激活现有菜单，需要激活父级菜单时使用")
    affix_tab: Optional[bool] = Field(default=None, description="是否固定标签")
    affix_tab_order: Optional[int] = Field(default=None, description="固定标签页的顺序")
    authority: Optional[List[str]] = Field(default=[], description="需要特定的角色标识才可以访问")
    badge: Optional[str] = Field(default=None, description="徽标")
    badge_type: Optional[str] = Field(default=None, description="徽标类型")
    badge_variants: Optional[str] = Field(default=None, description="徽标颜色")
    hide_children_in_menu: Optional[bool] = Field(default=None, description="当前路由的子级在菜单中不展现")
    hide_in_breadcrumb: Optional[bool] = Field(default=None, description="当前路由在面包屑中不展现")
    hide_in_menu: Optional[bool] = Field(default=None, description="当前路由在菜单中不展现")
    hide_in_tab: Optional[bool] = Field(default=None, description="当前路由在标签页不展现")
    icon: Optional[str] = Field(default=None, description="图标（菜单/tab）")
    iframe_src: Optional[str] = Field(default=None, description="iframe 地址")
    ignore_access: Optional[bool] = Field(default=None, description="忽略权限，直接可以访问")
    keep_alive: Optional[bool] = Field(default=None, description="开启KeepAlive缓存")
    link: Optional[str] = Field(default=None, description="外链-跳转路径")
    loaded: Optional[bool] = Field(default=None, description="路由是否已经加载过")
    max_num_of_open_tab: Optional[int] = Field(default=None, description="标签页最大打开数量")
    menu_visible_with_forbidden: Optional[bool] = Field(default=None, description="菜单可以看到，但是访问会被重定向到403")
    no_basic_layout: Optional[bool] = Field(default=None, description="当前路由不使用基础布局（仅在顶级生效）")
    open_in_new_window: Optional[bool] = Field(default=None, description="在新窗口打开")
    order: Optional[int] = Field(default=None, description="用于路由->菜单排序")
    query: Optional[str] = Field(default=None, description="菜单所携带的参数")
    title: Optional[str] = Field(default=None, description="标题名称")

    model_config = ConfigDict(
        alias_generator=snake_to_camel,
        populate_by_name=True,
        from_attributes=True,
        extra="allow"
    )
