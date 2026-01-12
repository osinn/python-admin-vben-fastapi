from fastapi import APIRouter, Depends, Request, Body

from apps.modules.sys.basis.routers import user_router, role_router, menu_router, post_router, dept_router, \
    sys_config_router, dict_item_router, dict_router
from apps.modules.sys.scheduler.routers import job_group_router, job_scheduler_router

app_router = APIRouter()
app_router.include_router(user_router, prefix="/sys", tags=["用户管理"])
app_router.include_router(role_router, prefix="/sys", tags=["角色管理"])
app_router.include_router(menu_router, prefix="/sys", tags=["菜单管理"])
app_router.include_router(post_router, prefix="/sys", tags=["岗位管理"])
app_router.include_router(dept_router, prefix="/sys", tags=["部门管理"])
app_router.include_router(sys_config_router, prefix="/sys", tags=["系统参数管理"])
app_router.include_router(dict_router, prefix="/sys", tags=["字典管理"])
app_router.include_router(dict_item_router, prefix="/sys", tags=["字典项管理"])
app_router.include_router(job_group_router, prefix="/job", tags=["任务调度-任务组管理"])
app_router.include_router(job_scheduler_router, prefix="/job", tags=["任务调度-任务调度管理"])
