from typing import Optional
from pydantic import Field
from core.framework.common_schemas import BaseModelSchema

class SysDictItemAddParam(BaseModelSchema):

    dict_id: int = Field(description="字典ID")
    dict_item_code: str = Field(description="字典项编码")
    dict_item_name:str = Field(description="字典项名称")
    sort: Optional[int] = Field(default=0, description="排序")

class SysDictItemEditParam(SysDictItemAddParam):
    id: int = Field(description="唯一ID")