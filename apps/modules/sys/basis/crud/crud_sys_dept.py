from typing import List

from apps.modules.sys.basis.schemas.sys_dept import SysDeptSchema
from core.framework.crud_async_session import AsyncGenericCRUD

class CrudSysDept:

    @classmethod
    async def get_dept_all_tree(cls, extend_data: bool, crud_async_session: AsyncGenericCRUD) -> List[SysDeptSchema]:
        model_info_all = await crud_async_session.get_model_info_all(v_schema=SysDeptSchema)
        if extend_data and len(model_info_all) == 0:
            dept_ids = set()
            for dept in model_info_all:
                dept_ids.add(dept.id)

            sql = [
                """
                    SELECT
                      dl.dept_id,
                      dl.user_id,
                      u.nickname as user_name
                    FROM
                      tbl_sys_user u
                        JOIN tbl_sys_dept_leader dl ON dl.user_id = u.id and dl.dept_id = :dept_ids
                """
            ]
            user_dept_data = await crud_async_session.execute_sql(" ".join(sql), {dept_ids: dept_ids})
            dept_user_map = {}
            for item in user_dept_data:
                dept_id = item["dept_id"]
                user_id = item["user_id"]
                user_name = item["user_name"]
                if dept_id not in dept_user_map:
                    dept_user_map[dept_id] = {"user_ids": [], "user_names": []}
                dept_user_map[dept_id]["user_ids"].append(user_id)
                dept_user_map[dept_id]["user_names"].append(user_name)

            for dept in model_info_all:
                current_dept_id = getattr(dept, "dept_id", None)

                user_info = dept_user_map.get(current_dept_id, {"user_ids": [], "user_names": []})
                user_ids = user_info["user_ids"]
                user_name_str = ",".join(user_info["user_names"])

                dept.dept_leader_user_names = user_name_str
                dept.dept_leader_user_ids = user_ids

        dept_tree = cls.to_dept_tree(model_info_all)
        return dept_tree

    @classmethod
    def to_dept_tree(cls, dept_list: List[object | SysDeptSchema]) -> List[object | SysDeptSchema]:
        if len(dept_list) == 1:
            return dept_list

        remove_ids = set()

        for parent in dept_list:
            for child in dept_list:
                if parent.id == child.parent_id:
                    if not parent.children:
                        parent.children = [child]
                    else:
                        parent.children.append(child)
                    remove_ids.add(child.id)

        result = [item for item in dept_list if item.id not in remove_ids]
        return result
