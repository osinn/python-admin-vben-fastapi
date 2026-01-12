from typing import Optional
from pydantic import Field
from core.framework.common_schemas import BaseModelSchema

class JobGroupAddParam(BaseModelSchema):
    group_name: str = Field(description="任务组名称")

class JobGroupEditParam(JobGroupAddParam):
    id: int = Field(description="任务组唯一ID")

class JobGroupPageParam(BaseModelSchema):
    page_num: int = Field(default=1, description="当前页，默认1（从1开始）")
    page_size: int = Field(default=10, description="每页行数，默认10")
    group_name: Optional[str] = Field(default=None, description="任务组名称")
