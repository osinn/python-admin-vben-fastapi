from apps.modules.sys.basis.params.sys_dict import SysDictPageParam
from apps.modules.sys.basis.schemas.sys_dict import SysDictSchema
from core.framework.crud_async_session import AsyncGenericCRUD

async def get_page_dict_list(sys_dict_page_param: SysDictPageParam,
                    crud_async_session: AsyncGenericCRUD):
    sql = [
        """
        select * from tbl_sys_dict where is_deleted = 0
        """
    ]
    # 搜索关键字：字典编码/字典名称
    if sys_dict_page_param.search_key:
        sql.append(
            """
                and (
                dict_code like concat('%', :search_key, '%')
                or dict_name like concat('%', :search_key, '%')
              )
            """
        )
    if sys_dict_page_param.is_default:
        sql.append(" and is_default = :is_default")
    if sys_dict_page_param.status:
        sql.append(" and status = :status")

    sql.append(" order by id desc")
    page_vo = await crud_async_session.page_select_model(" ".join(sql), sys_dict_page_param.__dict__, v_schema=SysDictSchema)
    return page_vo
