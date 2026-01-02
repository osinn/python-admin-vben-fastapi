from fastapi import APIRouter, Depends, Request, Body

from apps.modules.sys.basis.routers import user_router

app_router = APIRouter()
app_router.include_router(user_router, prefix="/sys", tags=["用户管理"])