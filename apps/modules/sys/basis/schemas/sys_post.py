from typing import Optional
from pydantic import Field
from core.framework.common_schemas import BaseSchema

class SysPostSchema(BaseSchema):

    post_code: Optional[str] = Field(default=None, description="岗位编码")
    name: Optional[str] = Field(default=None, description="岗位名称")
    remarks: Optional[str] = Field(default=None, description="备注")
    sort: Optional[int] = Field(default=None, description="排序")
    status: Optional[int] = Field(default=None, description="状态 1-正常；2-停用")