from fastapi import APIRouter, Depends

from apps.modules.sys.monitor.crud.crud_sys_http_log import CrudSysHttpLog
from apps.modules.sys.monitor.models.sys_http_log import SysHttpLogModel
from apps.modules.sys.monitor.params.sys_http_log import SysLoginLogPageParam
from core.framework.crud_async_session import AsyncGenericCRUD, crud_getter
from core.framework.response import SuccessResponse

sys_http_log_router = APIRouter()

@sys_http_log_router.post("/get_login_log_info_list", summary="登录日志查询")
async def get_login_log_info_list(sys_login_log_page_param: SysLoginLogPageParam,
                              crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysHttpLogModel))):
    login_log_info_list = await CrudSysHttpLog.get_login_log_info_list(sys_login_log_page_param, crud_async_session)
    return SuccessResponse(login_log_info_list)
