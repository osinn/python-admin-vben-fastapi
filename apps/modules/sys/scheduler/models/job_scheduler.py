from core.framework.database import BaseEntity
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String
from sqlalchemy.dialects.mysql import BIGINT

class JobSchedulerModel(BaseEntity):
    __tablename__ = "tbl_job_scheduler"

    job_group_id: Mapped[int] = mapped_column(BIGINT, nullable=False, default=None, comment="任务组ID")
    job_id: Mapped[str] = mapped_column(String(100), nullable=False, comment="任务唯一ID")
    trigger_type: Mapped[int] = mapped_column(Integer, nullable=False, comment="触发器类型：1-date、2-interval、3-cron")
    trigger_condition: Mapped[str] = mapped_column(String(255), nullable=False, comment="触发器触发条件")
    remarks: Mapped[str] = mapped_column(String(255), nullable=False, default="", comment="备注")
    author: Mapped[str] = mapped_column(String(64), nullable=False, default="", comment="作者")
    alarm_email: Mapped[str] = mapped_column(String(255), comment="报警邮件")
    executor_handler: Mapped[str] = mapped_column(String(255), nullable=False, comment="执行器任务handler(调用函数名称)")
    executor_param: Mapped[str] = mapped_column(String(512), comment="执行器任务参数")
    job_status: Mapped[int] = mapped_column(Integer, nullable=False, comment="任务调度状态，1-运行，2-暂停")
