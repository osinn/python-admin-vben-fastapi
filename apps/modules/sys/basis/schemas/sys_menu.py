from typing import Optional
from pydantic import Field
from core.framework.common_schemas import BaseSchema

from datetime import datetime




class SysMenuSchema(BaseSchema):

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