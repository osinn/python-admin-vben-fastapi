from core.framework.database import Base
from sqlalchemy.orm import Mapped, mapped_column

from sqlalchemy.dialects.mysql import BIGINT

from core.utils.Snowflake import snowflake


class SysUserPostModel(Base):
    __tablename__ = "tbl_sys_user_post"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, comment='主键ID',
                                    default=lambda: str(snowflake.generate_id()),
                                    server_default=str(snowflake.generate_id())
                                    )

    user_id: Mapped[int] = mapped_column(BIGINT, nullable=False, comment="用户ID")
    post_id: Mapped[int] = mapped_column(BIGINT, nullable=False, comment="岗位ID")
