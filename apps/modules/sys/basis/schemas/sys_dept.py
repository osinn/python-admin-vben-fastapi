from typing import Optional, List
from pydantic import Field
from core.framework.common_schemas import BaseSchema

from datetime import datetime




class SysDeptSchema(BaseSchema):

    parent_id: Optional[int] = Field(default=None, description="父部门ID")
    name: Optional[str] = Field(default=None, description="部门名称")
    ancestors: Optional[str] = Field(default=None, description="祖级列表")
    org_type: Optional[int] = Field(default=None, description="机构类型 1公司；2部门；3小组；4其他")
    sort: Optional[int] = Field(default=None, description="排序")
    remarks: Optional[str] = Field(default=None, description="备注")
    status: Optional[int] = Field(default=None, description="状态 1-正常；2-停用")
    dept_leader_user_names: Optional[str] = Field(default=None, description="部门领导名称")
    dept_leader_user_ids: Optional[List[int]] = Field(default=None, description="部门领导ID")
    disabled: Optional[bool] = Field(default=None, description="是否禁用，true-禁用，false-不禁用")
    children: Optional[List["SysDeptSchema"]] = Field(default=[], description="子节点")