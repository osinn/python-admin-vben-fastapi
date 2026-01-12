from typing import Optional

from pydantic import Field

from core.framework.common_schemas import BaseModelSchema

class SysDictAddParam(BaseModelSchema):

    dict_code: str = Field(description="字典编码")
    dict_name: str = Field(description="字典名称")
    remarks: Optional[str] = Field(default=None, description="备注")
    status: bool = Field(description="状态 false-正常；true-停用")

class SysDictEditParam(SysDictAddParam):
    id: int = Field(description="唯一ID")

class SysDictPageParam(BaseModelSchema):
    page_num: int = Field(default=1, description="当前页，默认1（从1开始）")
    page_size: int = Field(default=10, description="每页行数，默认10")
    search_key: Optional[str] = Field(default=None, description="搜索关键字：字典编码/字典名称")
    status: Optional[bool] = Field(default=None, description="状态 false-正常；true-禁用")
    is_default: Optional[bool] = Field(default=None, description="是否系统默认账号 false-不是；true-是")
