from typing import Optional

from pydantic import Field, BaseModel

from core.framework.common_schemas import BaseModelSchema


class SysMenuAddParam(BaseModelSchema):

    type: Optional[str] = Field(description="菜单类型 dir目录；menu菜单；button按钮")
    name: Optional[str] = Field(description="菜单名称")
    parent_id: Optional[int] = Field(default=0, init=True, description="上级菜单")
    path: Optional[str] = Field(description="路由地址")
    redirect: Optional[str] = Field(default=None)
    component: Optional[str] = Field(default=None, description="组件路径")
    status: Optional[int] = Field(description="状态 1-正常；2-停用")
    auth_code: Optional[str] = Field(default=None, description="权限标识")
    sort: Optional[int] = Field(default=1, init=True, description="排序")
    remarks: Optional[str] = Field(default="", description="备注")
    meta: Optional[str] = Field(default=None)

class SysMenuEditParam(SysMenuAddParam):
    id: int = Field(default=0, description="唯一ID")

class SysMenuTreeQueryParam(BaseModelSchema):
    status: Optional[bool] = Field(default=None, description="状态 false-正常；true-停用")

class SysMenuCheckExistsParam(BaseModelSchema):
    """
    检查菜单是否存在参数
    """
    id: Optional[int] = Field(default=None, description="菜单ID")
    key: Optional[str] = Field(default="", description="检查值是否存在")