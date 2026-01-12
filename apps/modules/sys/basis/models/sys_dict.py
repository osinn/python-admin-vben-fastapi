from core.framework.database import BaseEntity
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Boolean, DateTime, String

class SysDictModel(BaseEntity):
    __tablename__ = "tbl_sys_dict"

    dict_code: Mapped[str] = mapped_column(String(128), nullable=False, comment="字典编码")
    dict_name: Mapped[str] = mapped_column(String(128), nullable=False, comment="字典名称")
    remarks: Mapped[str] = mapped_column(String(512), comment="备注")
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, comment="状态 0-正常；1-停用")
    is_default: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, comment="是否默认：0-不是：1-默认")