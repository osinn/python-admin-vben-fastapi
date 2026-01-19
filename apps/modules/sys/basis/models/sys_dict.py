from core.framework.database import BaseEntity
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Boolean, DateTime, String, Integer


class SysDictModel(BaseEntity):
    __tablename__ = "tbl_sys_dict"

    dict_code: Mapped[str] = mapped_column(String(128), nullable=False, comment="字典编码")
    dict_name: Mapped[str] = mapped_column(String(128), nullable=False, comment="字典名称")
    remarks: Mapped[str] = mapped_column(String(512), comment="备注")
    status: Mapped[int] = mapped_column(Integer, nullable=False, default=1, comment="状态 1-正常；2-停用")
    is_default: Mapped[int] = mapped_column(Integer, nullable=False, default=2, comment="是否默认：1-是：2-非默认")