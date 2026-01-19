from datetime import datetime
from typing import Optional, List

from pydantic import Field, BaseModel

from core.framework.common_schemas import BaseModelSchema


class SysRoleAddParam(BaseModelSchema):
    role_code: Optional[str] = Field(description="角色编码")
    name: Optional[str] = Field(description="角色名称")
    remarks: Optional[str] = Field(default="", description="备注")
    sort: Optional[str] = Field(default=0, description="排序")
    status: Optional[int] = Field(default=1, description="状态 1正常；2停用")

class SysRoleEditParam(SysRoleAddParam):
    id: int = Field(default=0, description="唯一ID")

class SysRolePageParam(BaseModelSchema):
    page_num: int = Field(default=1, description="当前页，默认1（从1开始）")
    page_size: int = Field(default=10, description="每页行数，默认10")
    search_key: Optional[str] = Field(default=None,description="搜索关键字：角色编码/角色名称")
    status: Optional[int] = Field(default=None, description="状态 1-正常；2-停用")
    start_created_time: Optional[datetime] = Field(default=None, description="创建时间 开始时间")
    end_created_time: Optional[datetime] = Field(default=None, description="创建时间 结束时间")

class SysRoleAssignMenuParam(BaseModelSchema):
    """
    分配权限参数
    """
    role_id: int = Field(default=1, description="角色ID不能为空")
    menu_ids: List[int] = Field(default=1, description="菜单组")