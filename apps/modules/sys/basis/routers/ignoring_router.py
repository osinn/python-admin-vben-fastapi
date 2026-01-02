from fastapi import Depends, APIRouter

from core.framework.auth import Token, LoginAuth

ignor_router = APIRouter()

@ignor_router.post("/token", summary="请求登录-获取token", tags=["登录认证"])
async def login_for_access_token(
    token: Token = Depends(LoginAuth())
) -> Token:
    return token