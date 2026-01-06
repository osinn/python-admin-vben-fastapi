from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field

class SysUserAddParam(BaseModel):
    account: str = Field(description="账号")
    nickname: str = Field(description="昵称")
    password: Optional[str] = Field(default=None, description="密码")
    avatar: Optional[str] = Field(default=None, description="头像")
    email: Optional[str] = Field(default=None, description="邮箱")
    phone: Optional[str] = Field(default=None, description="手机号")
    staff_number: Optional[str] = Field(default=None, description="工号")
    birthday: Optional[datetime] = Field(default=None, description="生日")
    sex: int = Field(default=3, description="性别 1-男；2-女；3未知")
    dept_id: Optional[int] = Field(default=None, description="部门ID")
    sort: int = Field(default=0, description="排序")
    remarks: Optional[str] = Field(default=None, description="备注")
    status: int = Field(default=0, description="状态 0正常；1停用")


class SysUserEditParam(SysUserAddParam):
    id: int = Field(default=0, description="唯一ID")

class SysUserPageParam(BaseModel):
    page_num: int = Field(default=1, description="当前页，默认1（从1开始）")
    page_size: int = Field(default=10, description="每页行数，默认10")
    search_key: Optional[str] = Field(default=None,description="搜索关键字：用户名称/账号/手机号/工号/邮箱")
    sex: Optional[int] = Field(default=None,description="性别 1-男；2-女；3未知")
    dept_id: Optional[int] = Field(default=None,description="部门ID")
    status: Optional[int] = Field(default=None,description="状态 0正常；1停用")