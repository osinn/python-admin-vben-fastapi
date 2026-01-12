from typing import Optional

from pydantic import Field

from core.framework.common_schemas import BaseModelSchema

class SysDeptPageParam(BaseModelSchema):
    page_num: int = Field(default=1, description="当前页，默认1（从1开始）")
    page_size: int = Field(default=10, description="每页行数，默认10")
    name: Optional[str] = Field(default=None, description="搜索部门名称")

class SysDeptAddParam(BaseModelSchema):
    parent_id: int = Field(default=None, description="父部门ID")
    name: str = Field(description="部门名称")
    org_type: int = Field(default=1, description="机构类型 1公司；2部门；3小组；4其他")
    sort: int = Field(default=1, description="排序")
    remarks: str = Field(default="", description="备注")
    status: bool = Field(default=False, description="状态 false正常；true-停用")

class SysDeptEditParam(BaseModelSchema):
    id: int = Field(description="唯一ID")
