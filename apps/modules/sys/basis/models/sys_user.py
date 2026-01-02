from core.framework.database import BaseEntity
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Boolean, DateTime, Integer, String

from datetime import datetime


class SysUserModel(BaseEntity):
    __tablename__ = "tbl_sys_user"

    account: Mapped[str] = mapped_column(String(128), comment="账号")
    password: Mapped[str] = mapped_column(String(128), comment="密码")
    psw_modified: Mapped[bool] = mapped_column(Boolean, nullable=False, comment="修改密码标记 0未修改；1已修改")
    nickname: Mapped[str] = mapped_column(String(128), comment="昵称")
    avatar: Mapped[str] = mapped_column(String(128), comment="头像")
    email: Mapped[str] = mapped_column(String(128), comment="邮箱")
    phone: Mapped[str] = mapped_column(String(32), comment="手机号")
    staff_number: Mapped[str] = mapped_column(String(32), comment="工号")
    birthday: Mapped[datetime] = mapped_column(DateTime, comment="生日")
    sex: Mapped[int] = mapped_column(Integer, comment="性别 1-男；2-女；3未知")
    dept_id: Mapped[str] = mapped_column(String(32), comment="部门ID")
    lock_account: Mapped[int] = mapped_column(Integer, nullable=False, comment="锁定标记 0正常；1锁定")
    sort: Mapped[int] = mapped_column(Integer, nullable=False, comment="排序")
    remarks: Mapped[str] = mapped_column(String(512), comment="备注")
    status: Mapped[bool] = mapped_column(Boolean, comment="状态 0正常；1停用")
    is_default: Mapped[bool] = mapped_column(Boolean, nullable=False, comment="是否系统默认账号")
