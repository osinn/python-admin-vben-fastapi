from fastapi import APIRouter, Depends, Request, Body

from apps.modules.sys.basis.routers import user_router, role_router, menu_router, post_router

app_router = APIRouter()
app_router.include_router(user_router, prefix="/sys", tags=["用户管理"])
app_router.include_router(role_router, prefix="/sys", tags=["角色管理"])
app_router.include_router(menu_router, prefix="/sys", tags=["菜单管理"])
app_router.include_router(post_router, prefix="/post", tags=["岗位管理"])
