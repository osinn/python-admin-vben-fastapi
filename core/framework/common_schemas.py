
"""
分页
"""
import re
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, ConfigDict


class PageVo(BaseModel):
    total: int = Field(description="总数")
    items:list = Field(default=None, description="分页数据")

    def __init__(self, total: int, data: List = None):
        super().__init__(total=total, data=data)
        self.total = total
        self.items = data
    class Config:
        arbitrary_types_allowed = True


def camel_to_snake(name: str) -> str:
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def snake_to_camel(snake_str: str) -> str:
    components = snake_str.split('_')
    return components[0] + ''.join(x.capitalize() for x in components[1:])

class BaseModelSchema(BaseModel):
    """
    赋值时驼峰转下划线赋值对象属性，响应数据时将下划线转驼峰
    """
    model_config = ConfigDict(
        # alias_generator=snake_to_camel,
        # populate_by_name=True,
        from_attributes=True,
        # extra="allow"
    )

    # def model_dump(self, **kwargs):
    #     # 序列化时下划线是否转驼峰
    #     by_alias = kwargs.get("by_alias", True)
    #     kwargs.setdefault("by_alias", by_alias)
    #     return super().model_dump(**kwargs)

class BaseSchema(BaseModelSchema):

    id: int = Field(default=0, description="唯一ID")
    created_time: datetime = Field(default=None,description='创建时间 yyyy-MM-dd HH:mm:ss')
    created_by: int = Field(default=None,description='创建人ID')
    # 允许为空
    updated_time: Optional[datetime] = Field(default=None,description='更新时间 yyyy-MM-dd HH:mm:ss')
    # 允许为空
    updated_by: Optional[int] = Field(default=None,description='更新人ID')