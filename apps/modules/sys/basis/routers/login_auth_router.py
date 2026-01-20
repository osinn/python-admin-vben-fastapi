from typing import List

from fastapi import Depends, APIRouter, Request

from apps.modules.sys.basis.crud.crud_sys_menu import CrudSysMenu
from apps.modules.sys.basis.models.sys_menu import SysMenuModel
from apps.modules.sys.basis.schemas.sys_menu import RouteItemSchema
from core.constants.auth_constant import CACHE_OFFLINE_PREFIX
from core.framework.auth import Token, LoginAuth
from core.framework.cache_tools import cache
from core.framework.crud_async_session import AsyncGenericCRUD, crud_getter
from core.framework.response import SuccessResponse
from core.utils.rsa_utils import generate_rsa_keypair_b64

ignore_router = APIRouter()
login_auth_router = APIRouter()

@ignore_router.post("/auth/login", summary="请求登录-获取token", tags=["登录认证"])
async def login_for_access_token(token: Token = Depends(LoginAuth())):
    return SuccessResponse({"accessToken": token.access_token})

@ignore_router.get("/auth/get_auth_key", summary="获取加密公钥", tags=["登录认证"])
async def login_for_access_token(ticket: str):
    public_key = await cache.get("rsa:public:" + ticket)
    if public_key:
        return SuccessResponse(public_key)
    else:
        pub_key, pri_key = generate_rsa_keypair_b64()
        await cache.set("rsa:public:" + ticket, pub_key, 1000 * 60)
        await cache.set("rsa:private:" + ticket, pri_key, 1000 * 60)
        return SuccessResponse(pub_key)

@login_auth_router.get("/user/info", summary="获取当前用户信息", tags=["登录认证"])
async def get_user_info(request: Request):
    user = getattr(request.state, "user", None)
    return SuccessResponse(user)

@login_auth_router.get("/menu/all", summary="获取用户权限全部菜单", tags=["登录认证"])
async def get_route_menu_list(request: Request, crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysMenuModel))):
    user = getattr(request.state, "user", None)
    route_item: List[RouteItemSchema] = await CrudSysMenu.get_route_menu_list(user["id"], user["is_admin"], crud_async_session)
    return SuccessResponse(route_item)

@login_auth_router.get("/auth/codes", summary="获取用户所有权限编码", tags=["登录认证"])
async def get_route_menu_codes(request: Request, crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysMenuModel))):
    user = getattr(request.state, "user", None)
    route_menu_codes: List[str] = await CrudSysMenu.get_route_menu_codes(user["id"], user["is_admin"], crud_async_session)
    return SuccessResponse(route_menu_codes)

@login_auth_router.post("/auth/logout", summary="退出登录", tags=["登录认证"])
async def logout(request: Request):
    user = getattr(request.state, "user", None)
    await cache.delete(CACHE_OFFLINE_PREFIX + user["sub"])
    return SuccessResponse("OK")