from datetime import datetime
from typing import Optional

from pydantic import Field

from core.framework.common_schemas import BaseModelSchema


class SysConfigAddParam(BaseModelSchema):

    config_group_name: Optional[str] = Field(description="配置组名称")
    config_name: Optional[str] = Field(description="参数名称")
    config_key: Optional[str] = Field(description="参数键名")
    config_value: Optional[str] = Field(description="参数键值")
    remarks: Optional[str] = Field(default=None, description="备注")
    status: Optional[bool] = Field(default=None, description="状态 false-正常；true-禁用")

class SysConfigEditParam(SysConfigAddParam):
    id: int = Field(description="唯一ID")

class SysConfigPageParam(BaseModelSchema):
    page_num: int = Field(default=1, description="当前页，默认1（从1开始）")
    page_size: int = Field(default=10, description="每页行数，默认10")
    search_key: Optional[str] = Field(default=None, description="搜索关键字：配置组名称/参数名称/参数键名/参数键值")
    status: Optional[bool] = Field(default=None, description="状态 false-正常；true-禁用")
    is_default: Optional[bool] = Field(default=None, description="是否系统默认账号 false-不是；true-是")
    start_created_time: Optional[datetime] = Field(default=None, description="创建时间 开始时间")
    end_created_time: Optional[datetime] = Field(default=None, description="创建时间 结束时间")
