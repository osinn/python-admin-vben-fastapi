from datetime import datetime
from typing import Optional
from pydantic import Field
from core.framework.common_schemas import BaseModelSchema

class SysLoginLogPageParam(BaseModelSchema):
    page_num: int = Field(default=1, description="当前页，默认1（从1开始）")
    page_size: int = Field(default=10, description="每页行数，默认10")
    log_type: Optional[str] = Field(default=None, description="日志类型，例如：LOGIN(登录类型)")
    search_key: Optional[str] = Field(default=None, description="搜索关键字：当前登录用户账号/用户昵称")
    start_created_time: Optional[datetime] = Field(default=None, description="创建时间 开始时间")
    end_created_time: Optional[datetime] = Field(default=None, description="创建时间 结束时间")
    status: Optional[int] = Field(default=None, description="状态,1-成功，2-失败")