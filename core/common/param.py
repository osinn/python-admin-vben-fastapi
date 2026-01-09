from typing import Optional

from pydantic import Field, BaseModel

from core.framework.common_schemas import BaseModelSchema


class ChangeStatusParam(BaseModel):
    """
    更改状态
    """
    id: int = Field(description="唯一ID")
    status: Optional[int] = Field(description="状态")


class ChangeSortParam(BaseModelSchema):
    """
    更改排序参数
    """
    id: int = Field(description="唯一ID")
    sort: int = Field(description="排序号")