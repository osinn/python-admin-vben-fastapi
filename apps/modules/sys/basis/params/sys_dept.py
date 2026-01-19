from typing import Optional, List

from pydantic import Field

from core.framework.common_schemas import BaseModelSchema

class SysDeptPageParam(BaseModelSchema):
    page_num: int = Field(default=1, description="当前页，默认1（从1开始）")
    page_size: int = Field(default=10, description="每页行数，默认10")
    name: Optional[str] = Field(default=None, description="搜索部门名称")

class SysDeptAddParam(BaseModelSchema):
    parent_id: int = Field(default=0, init=True, description="父部门ID")
    name: str = Field(description="部门名称")
    org_type: int = Field(default=1, description="机构类型 1公司；2部门；3小组；4其他")
    sort: int = Field(default=1, description="排序")
    remarks: str = Field(default="", description="备注")
    status: int = Field(default=1, description="状态 1-正常；2-停用")
    dept_leader_user_ids: List[int] = Field(default=None, exclude=True, description="部门领导-用户ID")

class SysDeptEditParam(SysDeptAddParam):
    id: int = Field(description="唯一ID")
