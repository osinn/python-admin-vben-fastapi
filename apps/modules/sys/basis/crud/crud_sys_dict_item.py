from typing import List

from apps.modules.sys.basis.schemas.sys_dict_item import SysDictItemSchema
from core.framework.crud_async_session import AsyncGenericCRUD

async def get_dict_item_list_all_of_dict_id(dict_id: int, crud_async_session: AsyncGenericCRUD):
    sql = "select * from tbl_sys_dict_item where is_deleted = false and dict_id = :dict_id order by sort desc, id desc"

    data_list: List[SysDictItemSchema] = await crud_async_session.list_model("".join(sql), {"dict_id": dict_id}, v_schema=SysDictItemSchema)
    return data_list

async def delete_dict_item_of_dict_id(dict_id: int, crud_async_session: AsyncGenericCRUD):
    sql = "update tbl_sys_dict_item set is_deleted=true where dict_id = :dict_id"
    await crud_async_session.execute_sql("".join(sql), {"dict_id": dict_id})
