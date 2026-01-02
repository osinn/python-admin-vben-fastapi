from datetime import datetime, date
from typing import Any, TypeVar, Generic, Union, Dict

from fastapi.responses import ORJSONResponse as Response
from fastapi import status as http_status
from pydantic import BaseModel

from core.framework import status as http

# -------------------------- 1. 定义通用类型与统一响应模型 --------------------------
# 泛型类型变量，支持任意数据类型的data字段
T = TypeVar("T")

def _format_datetime(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {k: _format_datetime(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_format_datetime(item) for item in obj]
    elif isinstance(obj, datetime):
        return obj.strftime("%Y-%m-%d %H:%M:%S")
    elif isinstance(obj, date):
        return obj.strftime("%Y-%m-%d")
    elif isinstance(obj, int):
        return f"{obj}" if obj > 9007199254740992 else obj
    else:
        return obj


# 统一返回数据格式模型（核心）
class ApiResponse(BaseModel, Generic[T]):
    code: int = 200                # 业务状态码，默认200成功
    data: Union[T, list] = []      # 数据体，默认空列表，支持任意类型
    message: str = ""              # 提示信息，默认空字符串
    class Config:
        arbitrary_types_allowed = True

    def model_dump(self, *args, **kwargs) -> Dict[str, Any]:
        data = super().model_dump(*args, **kwargs)
        return _format_datetime(data)

    def model_dump_json(self, *args, **kwargs) -> str:
        import json
        data = self.model_dump(*args, **kwargs)
        return json.dumps(data, default=str)  # default=str 防止意外类型

# def SuccessResponse(data=None, message: str = "") -> Response:
#     return Response(
#         content=ApiResponse(code=200, data=data, message=message).model_dump(),
#         headers={"X-Trace-Id": "123456789", "X-App-Version": "v1.0"}  # 自定义头
#     )
class SuccessResponse(Response):
    """
    成功响应
    Args:
        data: 继承pydantic模型的实例
        exclude_attrs: 要排除的属性列表
    """
    def __init__(self, data=None, message="success", code=http.HTTP_SUCCESS, status=http_status.HTTP_200_OK, **kwargs):
        super().__init__(content=ApiResponse(code=200, data=data, message=message).model_dump(), status_code=status)
# def success_response(data: Any = [], message: str = "") -> JSONResponse:
#     res = ApiResponse(code=200, data=data, message=message)
#     return JSONResponse(content=res.dict(), headers={"X-Request-Id": "xxx-xxx"})

class ErrorResponse(Response):
    """
    失败响应
    """

    def __init__(self, message=None, code=http.HTTP_ERROR, status=http_status.HTTP_200_OK):
        super().__init__(content=ApiResponse(code=code, message=message).model_dump(), status_code=status)

