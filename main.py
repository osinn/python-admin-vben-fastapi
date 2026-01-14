
from fastapi import FastAPI, Depends, APIRouter
from pydantic import BaseModel, Field

import uvicorn
from starlette.middleware.cors import CORSMiddleware

from apps.app_router import app_router

from apps.modules.sys.basis.routers.login_auth_router import login_auth_router, ignore_router
from config import settings
from core.framework.auth import AuthAuthorize
from core.framework.exception import register_exception


# 2. 定义统一的错误响应模型（可选，用于规范格式）
class ErrorResponse(BaseModel):
    code: int = Field(description="错误码")
    msg: str = Field(description="错误信息")

app = FastAPI(
    lifespan=settings.lifespan
)

# 公共（无需登录）的路由
public_router = APIRouter(prefix="/api")
public_router.include_router(ignore_router)

# 需登录的路由（统一加依赖）
auth_authorize_router = APIRouter(prefix="/api", dependencies=[Depends(AuthAuthorize())]) # 全局注入所有路由自动应用此依赖登录认证
auth_authorize_router.include_router(app_router)
auth_authorize_router.include_router(login_auth_router) # 登录成功后查询数据需要登录的接口
# 分别挂载
app.include_router(public_router)          # 无认证
app.include_router(auth_authorize_router)  # 有认证



# 全局异常捕捉处理
register_exception(app)

# 跨域解决
if settings.CORS_ORIGIN_ENABLE:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOW_ORIGINS,
        allow_credentials=settings.ALLOW_CREDENTIALS,
        allow_methods=settings.ALLOW_METHODS,
        allow_headers=settings.ALLOW_HEADERS
    )

if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=5320, reload=settings.DEBUG)
    """
    启动项目

    factory: 在使用 uvicorn.run() 启动 ASGI 应用程序时，可以通过设置 factory 参数来指定应用程序工厂。
    应用程序工厂是一个返回 ASGI 应用程序实例的可调用对象，它可以在启动时动态创建应用程序实例。
    """
    # uvicorn.run(app='main:app', host="127.0.0.1", port=8000, reload=True, lifespan="on", factory=True)

