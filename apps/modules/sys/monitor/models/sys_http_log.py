from core.framework.database import  Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Boolean, DateTime, String, Text, func, Integer
from sqlalchemy.dialects.mysql import BIGINT

from datetime import datetime

from core.utils.Snowflake import snowflake


class SysHttpLogModel(Base):
    __tablename__ = "tbl_sys_http_log"

    id:  Mapped[int] = mapped_column(BIGINT, primary_key=True, comment='主键ID',
                                     default=lambda: str(snowflake.generate_id()),
                                     server_default=str(snowflake.generate_id())
                                     )

    user_id: Mapped[int] = mapped_column(BIGINT, comment="当前登录用户id")
    account: Mapped[str] = mapped_column(String(20), comment="当前登录用户账号")
    nickname: Mapped[str] = mapped_column(String(255), comment="当前登录用户昵称")
    ip_address: Mapped[str] = mapped_column(String(50), comment="IP地址")
    ip_address_attr: Mapped[str] = mapped_column(String(100), comment="IP地址归属地")
    request_uri: Mapped[str] = mapped_column(String(255), comment="请求资源")
    request_headers: Mapped[str] = mapped_column(String(30), comment="请求头")
    request_params: Mapped[str] = mapped_column(Text, comment="请求参数")
    result_data: Mapped[str] = mapped_column(Text, comment="响应数据")
    request_method: Mapped[str] = mapped_column(String(30), nullable=False, comment="请求类型：POST/GET")
    class_method: Mapped[str] = mapped_column(String(255), comment="被调方法")
    business_module: Mapped[str] = mapped_column(String(50), nullable=False, comment="业务模块：业务模块主要是用在业务中台，区分业务，例如车辆模块、商城模块")
    module_name: Mapped[str] = mapped_column(String(255), nullable=False, comment="日志模块名称 业务模块下面的具体模块菜单-例如-用户管理")
    source: Mapped[str] = mapped_column(String(50), nullable=False, comment="日志来源")
    log_type: Mapped[str] = mapped_column(String(50), nullable=False, comment="日志类型")
    action_desc: Mapped[str] = mapped_column(String(255), nullable=False, comment="动作描述")
    status: Mapped[int] = mapped_column(Integer, nullable=False, comment="状态,1-成功，2-失败")
    operate_type: Mapped[str] = mapped_column(String(30), nullable=False, comment="操作类型，例如增删改查、登录")
    execution_time: Mapped[str] = mapped_column(String(100), nullable=False, comment="执行耗时(毫秒单位)")
    exception_msg: Mapped[str] = mapped_column(Text, comment="异常信息")
    browser: Mapped[str] = mapped_column(String(100), nullable=False, comment="浏览器")
    os: Mapped[str] = mapped_column(String(100), nullable=False, comment="操作系统")
    mobile: Mapped[int] = mapped_column(Integer, nullable=False, comment="是否是移动端请求，1-是，2-不是")
    created_time: Mapped[datetime] = mapped_column(DateTime, default=func.now(), server_default=func.now(), comment='创建时间')