from typing import Optional
from pydantic import Field
from core.framework.common_schemas import BaseSchema

from datetime import datetime


class JobGroupSchema(BaseSchema):

    group_name: Optional[str] = Field(default=None, description="任务组名称")