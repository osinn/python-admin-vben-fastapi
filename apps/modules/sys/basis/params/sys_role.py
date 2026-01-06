from typing import Optional

from pydantic import Field, BaseModel

class SysRoleAddParam(BaseModel):
    role_code: Optional[str] = Field(description="角色编码")
    name: Optional[str] = Field(description="角色名称")
    remarks: Optional[str] = Field(default="", description="备注")
    sort: Optional[str] = Field(default=0, description="排序")
    status: Optional[str] = Field(default=0, description="状态 0正常；1停用")

class SysRoleEditParam(SysRoleAddParam):
    id: int = Field(default=0, description="唯一ID")

class SysRolePageParam(BaseModel):
    page_num: int = Field(default=1, description="当前页，默认1（从1开始）")
    page_size: int = Field(default=10, description="每页行数，默认10")
    search_key: Optional[str] = Field(default=None,description="搜索关键字：角色编码/角色名称")
    status: Optional[int] = Field(default=None,description="状态 0正常；1停用")