from typing import Optional
from core.framework.database import BaseEntity
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.dialects.mysql import BIGINT

from datetime import datetime


class SysMenuModel(BaseEntity):
    __tablename__ = "tbl_sys_menu"

    type: Mapped[str] = mapped_column(String(32), comment="菜单类型 dir目录；menu菜单；button按钮")
    name: Mapped[str] = mapped_column(String(128), comment="菜单名称")
    parent_id: Mapped[int] = mapped_column(BIGINT, nullable=False, comment="上级菜单")
    path: Mapped[str] = mapped_column(String(512), comment="路由地址")
    redirect: Mapped[str] = mapped_column(String(255))
    component: Mapped[str] = mapped_column(String(512), comment="组件路径")
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, comment="状态 0-正常；1-停用")
    auth_code: Mapped[str] = mapped_column(String(128), comment="权限标识")
    sort: Mapped[int] = mapped_column(Integer, nullable=False, comment="排序")
    remarks: Mapped[str] = mapped_column(String(512), comment="备注")
    meta: Mapped[str] = mapped_column(Text)
