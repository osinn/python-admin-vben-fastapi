from typing import Optional
from pydantic import Field
from core.framework.common_schemas import BaseSchema

class SysConfigSchema(BaseSchema):

    config_group_name: Optional[str] = Field(default=None, description="配置组名称")
    config_name: Optional[str] = Field(default=None, description="参数名称")
    config_key: Optional[str] = Field(default=None, description="参数键名")
    config_value: Optional[str] = Field(default=None, description="参数键值")
    remarks: Optional[str] = Field(default=None, description="备注")
    status: Optional[int] = Field(default=None, description="状态 1-正常；2-禁用")
    is_default: Optional[int] = Field(default=None, description="是否系统默认账号，1-默认，2-非默认")