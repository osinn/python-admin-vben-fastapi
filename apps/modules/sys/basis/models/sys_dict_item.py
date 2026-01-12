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
    sort: Mapped[int] = mapped_column(Integer, nullable=False, comment="排序")
    remarks: Mapped[str] = mapped_column(String(512), nullable=False, comment="备注")
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, comment="状态 0-启用；1-禁用")
    is_default: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, comment="是否默认")