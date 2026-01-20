from fastapi import APIRouter, Path, Depends

from apps.modules.sys.basis.crud.crud_sys_user import CrudSysUser
from apps.modules.sys.basis.models.sys_user import SysUserModel
from core.framework.auth import AuthValidation, get_online_user, deleted_online_user, fetch_online_user_all, PreAuthorize
from core.framework.crud_async_session import AsyncGenericCRUD, crud_getter
from core.framework.response import SuccessResponse

online_user_router = APIRouter()

@online_user_router.get("/get_online_user_all", summary="获取所有在线用户")
async def get_online_user_all(_ = Depends(PreAuthorize(permissions=["login:user:online"]))):
    online_user_all = await fetch_online_user_all()
    return SuccessResponse(online_user_all)

@online_user_router.put("/{sub}/offline", summary="强制在线用户下线")
async def offline(sub: str = Path(description="在线用户sub值"), _ = Depends(PreAuthorize(permissions=["login:user:offline"]))):
    await deleted_online_user(sub)
    return SuccessResponse("OK")

@online_user_router.put("/{sub}/refresh_user_permission", summary="刷新在线用户权限")
async def refresh_user_permission(sub: str = Path(description="在线用户sub值"),
                                  crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysUserModel)),
                                  _ = Depends(PreAuthorize(permissions=["login:user:refreshPermission"]))
                                  ):
    online_user = await get_online_user(sub)
    user_role_permissions = await CrudSysUser.get_sys_user_permission(online_user["id"], crud_async_session)
    online_user["roles"] = user_role_permissions
    await AuthValidation.save_online_user(sub, online_user)
    return SuccessResponse("OK")