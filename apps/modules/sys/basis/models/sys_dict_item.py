from typing import Optional
from core.framework.database import BaseEntity
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.dialects.mysql import BIGINT

from datetime import datetime




class SysDictItemModel(BaseEntity):
    __tablename__ = "tbl_sys_dict_item"

    dict_id: Mapped[int] = mapped_column(BIGINT, nullable=False, comment="字典ID")
    dict_item_code: Mapped[str] = mapped_column(String(128), nullable=False, comment="字典项编码")
    dict_item_name: Mapped[str] = mapped_column(String(128), nullable=False, comment="字典项名称")
    sort: Mapped[int] = mapped_column(Integer, nullable=False, default=1, comment="排序")
    remarks: Mapped[str] = mapped_column(String(512), nullable=False, default="", comment="备注")
    status: Mapped[int] = mapped_column(Integer, nullable=False, default=1, comment="状态 1-启用；2-禁用")
    is_default: Mapped[int] = mapped_column(Integer, nullable=False, default=2, comment="是否默认：1-是：2-非默认")