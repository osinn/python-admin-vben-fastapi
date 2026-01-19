from typing import Optional

from pydantic import Field

from core.framework.common_schemas import BaseSchema

class SysRoleSchema(BaseSchema):
    role_code: Optional[str] = Field(default=None, description="角色编码")
    name: Optional[str] = Field(default=None, description="角色名称")
    remarks: Optional[str] = Field(default=None, description="备注")
    sort: Optional[int] = Field(default=None, description="排序")
    status: Optional[int] = Field(default=None, description="状态 q正常；w停用")
    is_default: Optional[int] = Field(default=None, description="是否系统默认账号")