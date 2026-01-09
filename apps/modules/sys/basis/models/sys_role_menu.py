from core.framework.database import Base, BaseEntity
from sqlalchemy.orm import Mapped, mapped_column

from sqlalchemy.dialects.mysql import BIGINT

from core.utils.Snowflake import snowflake

class SysRoleMenuModel(Base):
    __tablename__ = "tbl_sys_role_menu"

    id:  Mapped[int] = mapped_column(BIGINT, primary_key=True, comment='主键ID',
                                     default=lambda: str(snowflake.generate_id()),
                                     server_default=str(snowflake.generate_id())
                                     )

    role_id: Mapped[int] = mapped_column(BIGINT, nullable=False, comment="角色ID")
    menu_id: Mapped[int] = mapped_column(BIGINT, nullable=False, comment="菜单ID")