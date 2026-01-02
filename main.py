
from fastapi import FastAPI
from pydantic import BaseModel, Field

import uvicorn
from starlette.middleware.cors import CORSMiddleware

from apps.app_router import app_router
from config import settings
from core.framework.exception import register_exception


# 2. 定义统一的错误响应模型（可选，用于规范格式）
class ErrorResponse(BaseModel):
    code: int = Field(description="错误码")
    msg: str = Field(description="错误信息")

app = FastAPI(
    lifespan=settings.lifespan
)

app.include_router(app_router)

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
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=settings.DEBUG)
    """
    启动项目

    factory: 在使用 uvicorn.run() 启动 ASGI 应用程序时，可以通过设置 factory 参数来指定应用程序工厂。
    应用程序工厂是一个返回 ASGI 应用程序实例的可调用对象，它可以在启动时动态创建应用程序实例。
    """
    # uvicorn.run(app='main:app', host="127.0.0.1", port=8000, reload=True, lifespan="on", factory=True)

