from core.framework.database import BaseEntity
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

class JobGroupModel(BaseEntity):
    __tablename__ = "tbl_job_group"

    group_name: Mapped[str] = mapped_column(String(50), nullable=False, comment="任务组名称")