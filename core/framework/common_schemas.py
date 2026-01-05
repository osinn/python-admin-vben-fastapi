
"""
分页
"""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class PageVo(BaseModel):
    total: int = Field(description="总数",strict=False)
    data:list = Field(description="分页数据")

    def __init__(self, total: int, data: List = None):
        self.total = total
        self.data = data
        super().__init__(total=total, data=data)
    class Config:
        arbitrary_types_allowed = True

class BaseSchema(BaseModel):

    id: int = Field(default=0, description="唯一ID")
    created_time: datetime = Field(description='创建时间 yyyy-MM-dd HH:mm:ss')
    created_by: int = Field(description='创建人ID')
    # 允许为空
    updated_time: Optional[datetime] = Field(description='更新时间 yyyy-MM-dd HH:mm:ss')
    # 允许为空
    updated_by: Optional[int] = Field(description='更新人ID')

    class Config:
        from_attributes = True  # SQLAlchemy 2.0+ 用这个（替代旧版的 orm_mode=True）