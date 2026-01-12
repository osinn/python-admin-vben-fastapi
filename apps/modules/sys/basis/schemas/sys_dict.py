from typing import Optional
from pydantic import Field
from core.framework.common_schemas import BaseSchema

class SysDictSchema(BaseSchema):

    dict_code: Optional[str] = Field(default=None, description="字典编码")
    dict_name: Optional[str] = Field(default=None, description="字典名称")
    remarks: Optional[str] = Field(default=None, description="备注")
    status: Optional[bool] = Field(default=None, description="状态 0-正常；1-停用")
    is_default: Optional[bool] = Field(default=None, description="是否默认：0-不是：1-默认")