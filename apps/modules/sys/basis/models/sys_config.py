from core.framework.database import BaseEntity
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Boolean, DateTime, String, Integer


class SysConfigModel(BaseEntity):
    __tablename__ = "tbl_sys_config"

    config_group_name: Mapped[str] = mapped_column(String(255), nullable=False, comment="配置组名称")
    config_name: Mapped[str] = mapped_column(String(128), comment="参数名称")
    config_key: Mapped[str] = mapped_column(String(128), comment="参数键名")
    config_value: Mapped[str] = mapped_column(String(512), comment="参数键值")
    remarks: Mapped[str] = mapped_column(String(512), comment="备注")
    status: Mapped[int] = mapped_column(Integer, nullable=False, default=0, comment="状态 1-正常；2-禁用")
    is_default: Mapped[int] = mapped_column(Integer, nullable=False, default=False, comment="是否系统默认账号，1-默认，2-非默认")