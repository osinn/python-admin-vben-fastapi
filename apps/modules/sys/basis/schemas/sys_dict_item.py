from typing import Optional
from pydantic import Field
from core.framework.common_schemas import BaseSchema

from datetime import datetime




class SysDictItemSchema(BaseSchema):

    dict_id: Optional[int] = Field(default=None, description="字典ID")
    dict_item_code: Optional[str] = Field(default=None, description="字典项编码")
    dict_item_name: Optional[str] = Field(default=None, description="字典项名称")
    sort: Optional[int] = Field(default=None, description="排序")
    remarks: Optional[str] = Field(default=None, description="备注")
    status: Optional[int] = Field(default=None, description="状态 1-启用；2-禁用")
    is_default: Optional[int] = Field(default=None, description="是否默认：1-是：2-非默认")