from typing import Optional
from core.framework.database import BaseEntity
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.dialects.mysql import BIGINT

from datetime import datetime




class SysPostModel(BaseEntity):
    __tablename__ = "tbl_sys_post"

    post_code: Mapped[str] = mapped_column(String(128), comment="岗位编码")
    name: Mapped[str] = mapped_column(String(128), comment="岗位名称")
    remarks: Mapped[str] = mapped_column(String(512), comment="备注")
    sort: Mapped[int] = mapped_column(Integer, nullable=False, comment="排序")
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, comment="状态 false-正常；true-停用")