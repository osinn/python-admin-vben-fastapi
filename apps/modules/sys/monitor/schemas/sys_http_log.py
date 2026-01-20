from datetime import datetime
from typing import Optional
from pydantic import Field, BaseModel, ConfigDict


class SysHttpLogSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )
    id: int = Field(description="唯一ID")
    user_id: Optional[int] = Field(default=None, description="当前登录用户id")
    account: Optional[str] = Field(default=None, description="当前登录用户账号")
    nickname: Optional[str] = Field(default=None, description="当前登录用户昵称")
    ip_address: Optional[str] = Field(default=None, description="IP地址")
    ip_address_attr: Optional[str] = Field(default=None, description="IP地址归属地")
    request_uri: Optional[str] = Field(default=None, description="请求资源")
    request_headers: Optional[str] = Field(default=None, description="请求头")
    request_params: Optional[str] = Field(default=None, description="请求参数")
    result_data: Optional[str] = Field(default=None, description="响应数据")
    request_method: Optional[str] = Field(default=None, description="请求类型：POST/GET")
    class_method: Optional[str] = Field(default=None, description="被调方法")
    business_module: Optional[str] = Field(default=None, description="业务模块：业务模块主要是用在业务中台，区分业务，例如车辆模块、商城模块")
    module_name: Optional[str] = Field(default=None, description="日志模块名称 业务模块下面的具体模块菜单-例如-用户管理")
    source: Optional[str] = Field(default=None, description="日志来源")
    log_type: Optional[str] = Field(default=None, description="日志类型")
    action_desc: Optional[str] = Field(default=None, description="动作描述")
    status: Optional[int] = Field(default=None, description="状态,1-成功，2-失败")
    operate_type: Optional[str] = Field(default=None, description="操作类型，例如增删改查、登录")
    execution_time: Optional[str] = Field(default=None, description="执行耗时(毫秒单位)")
    exception_msg: Optional[str] = Field(default=None, description="异常信息")
    browser: Optional[str] = Field(default=None, description="浏览器")
    os: Optional[str] = Field(default=None, description="操作系统")
    mobile: Optional[int] = Field(default=None, description="是否是移动端请求，1-是，2-不是")
    created_time: datetime = Field(default=None, description='创建时间 yyyy-MM-dd HH:mm:ss')