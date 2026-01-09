from core.framework.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, func
from sqlalchemy.dialects.mysql import BIGINT

from datetime import datetime

from core.utils.Snowflake import snowflake


class SysDeptPostModel(Base):
    __tablename__ = "tbl_sys_dept_post"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, comment='主键ID',
                                    default=lambda: str(snowflake.generate_id()),
                                    server_default=str(snowflake.generate_id())
                                    )

    dept_id: Mapped[int] = mapped_column(BIGINT, nullable=False, comment="部门Id")
    post_id: Mapped[int] = mapped_column(BIGINT, nullable=False, comment="岗位Id")

    created_time: Mapped[datetime] = mapped_column(DateTime,
                                                   default=func.now(),
                                                   server_default=func.now(), comment='创建时间')

    created_by: Mapped[int] = mapped_column(BIGINT, comment='创建人ID')
