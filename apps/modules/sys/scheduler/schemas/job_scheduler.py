from typing import Optional
from pydantic import Field
from core.framework.common_schemas import BaseSchema

class JobSchedulerSchema(BaseSchema):

    job_group_id: Optional[int] = Field(default=None, description="任务组ID")
    job_id: Optional[str] = Field(default=None, description="任务key唯一标识")
    trigger_type: Optional[int] = Field(default=None, description="触发器类型：1-date、2-interval、3-cron")
    trigger_condition: Optional[str] = Field(default=None, description="触发器触发条件")
    remarks: Optional[str] = Field(default=None, description="备注")
    author: Optional[str] = Field(default=None, description="作者")
    alarm_email: Optional[str] = Field(default=None, description="报警邮件")
    executor_handler: Optional[str] = Field(default=None, description="执行器任务handler(调用函数名称)")
    executor_param: Optional[str] = Field(default=None, description="执行器任务参数")