from core.framework.database import BaseEntity
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Boolean,Integer, String

class SysRoleModel(BaseEntity):
    """
    角色表
    """
    __tablename__ = "tbl_sys_role"

    role_code: Mapped[str] = mapped_column(String(128), comment="角色编码")
    name: Mapped[str] = mapped_column(String(128), comment="角色名称")
    remarks: Mapped[str] = mapped_column(String(512), comment="备注")
    sort: Mapped[int] = mapped_column(Integer, nullable=False, comment="排序", default=0)
    status: Mapped[int] = mapped_column(Integer, comment="状态 1正常；2停用", default=1)
    is_default: Mapped[int] = mapped_column(Integer, nullable=False, default=2, comment="是否系统默认账号，1-默认，2-非默认")




