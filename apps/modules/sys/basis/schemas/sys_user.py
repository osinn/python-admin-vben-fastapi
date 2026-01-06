from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field

from core.framework.common_schemas import BaseSchema


class SysUserSchema(BaseSchema):
    account: str = Field(..., description="账号")
    # password: Optional[str] = Field(default=None, description="密码")
    psw_modified: int = Field(default=0, description="修改密码标记 0未修改；1已修改")
    nickname: Optional[str] = Field(default=None, description="昵称")
    avatar: Optional[str] = Field(default=None, description="头像")
    email: Optional[str] = Field(default=None, description="邮箱")
    phone: Optional[str] = Field(default=None, description="手机号")
    staff_number: Optional[str] = Field(default=None, description="工号")
    birthday: Optional[datetime] = Field(default=None, description="生日")
    sex: int = Field(default=3, description="性别 1-男；2-女；3未知")
    dept_id: Optional[int] = Field(default=None, description="部门ID")
    lock_account: int = Field(default=0, description="锁定标记 0正常；1锁定")
    sort: int = Field(default=0, description="排序")
    remarks: Optional[str] = Field(default=None, description="备注")
    status: int = Field(default=0, description="状态 0正常；1停用")
    is_default: bool = Field(default=False, description="是否系统默认账号")
