from typing import Optional
from pydantic import Field
from core.framework.common_schemas import BaseSchema

class SysDictSchema(BaseSchema):

    dict_code: Optional[str] = Field(default=None, description="字典编码")
    dict_name: Optional[str] = Field(default=None, description="字典名称")
    remarks: Optional[str] = Field(default=None, description="备注")
    status: Optional[int] = Field(default=None, description="状态 1-正常；2停用")
    is_default: Optional[int] = Field(default=None, description="是否默认：1-是：2-非默认")