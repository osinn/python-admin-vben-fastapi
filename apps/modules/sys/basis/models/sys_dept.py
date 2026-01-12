from core.framework.database import BaseEntity
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Boolean, Integer, String
from sqlalchemy.dialects.mysql import BIGINT

from datetime import datetime

class SysDeptModel(BaseEntity):
    __tablename__ = "tbl_sys_dept"

    parent_id: Mapped[int] = mapped_column(BIGINT, comment="父部门ID")
    name: Mapped[str] = mapped_column(String(32), nullable=False, comment="部门名称")
    ancestors: Mapped[str] = mapped_column(String(1024), comment="祖级列表")
    org_type: Mapped[int] = mapped_column(Integer, comment="机构类型 1公司；2部门；3小组；4其他")
    sort: Mapped[int] = mapped_column(Integer, comment="排序")
    remarks: Mapped[str] = mapped_column(String(512), comment="备注")
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, comment="状态 false正常；true-停用")
