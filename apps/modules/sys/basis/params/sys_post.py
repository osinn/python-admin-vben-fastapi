from typing import Optional
from pydantic import Field
from core.framework.common_schemas import BaseSchema, BaseModelSchema


class SysPostQueryParam(BaseModelSchema):

    searchKey: Optional[str] = Field(default=None, description="岗位名称/岗位编码")
    status: Optional[bool] = Field(default=None, description="状态 false-正常；true-停用")

class SysPostAddParam(BaseModelSchema):
    post_code: Optional[str] = Field(default=None, description="岗位编码")
    name: Optional[str] = Field(default=None, description="岗位名称")
    remarks: Optional[str] = Field(default=None, description="备注")
    sort: Optional[int] = Field(default=None, description="排序")
    status: Optional[bool] = Field(default=None, description="状态 false-正常；true-停用")

class SysPostEditParam(SysPostAddParam):
    id: int = Field(default=0, description="唯一ID")

class DeptPostQueryParam(BaseModelSchema):
    """
    查询部门岗位参数
    """
    dept_id: int = Field(description="部门ID")
    checked: Optional[bool] = Field(default=None, description="是否选中,  true-则只查询选中的，false-则只查询未选中的，null-则查询所有")
    status: Optional[bool] = Field(default=None, description="状态 false-正常；true-停用")