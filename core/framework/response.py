from datetime import datetime, date
from typing import Any, TypeVar, Generic, Union, Dict

from fastapi.responses import ORJSONResponse as Response
from fastapi import status as http_status
from pydantic import BaseModel

from core.framework import status as http
from core.utils.JSONUtils import JSONUtils

# -------------------------- 1. 定义通用类型与统一响应模型 --------------------------
# 泛型类型变量，支持任意数据类型的data字段
T = TypeVar("T")

def _format_datetime(obj: Any) -> Any:
    if isinstance(obj, BaseModel):
        return _format_datetime(obj.model_dump(by_alias=True))
    elif isinstance(obj, dict):
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
    code: int = 200  # 业务状态码，默认200成功
    data: Union[T, list] = []  # 数据体，默认空列表，支持任意类型
    message: str = ""  # 提示信息，默认空字符串

    class Config:
        arbitrary_types_allowed = True

    # 移除写死的 by_alias=False，改为通过 kwargs 接收
    def model_dump(self, *args, **kwargs) -> Dict[str, Any]:
        # 关键：删除 *args（model_dump不支持位置参数），仅传递 kwargs
        data = super().model_dump(**kwargs)
        return _format_datetime(data)

    def model_dump_json(self, *args, **kwargs) -> str:
        # 同样删除 *args，仅传递 kwargs
        data = self.model_dump(**kwargs)
        return JSONUtils.dumps(data, default=str)


# 改造后的 SuccessResponse
class SuccessResponse(Response):
    # 新增 by_alias 参数，默认值设为 False（保持原有默认行为）
    def __init__(self, data=None, message="success", code=http.HTTP_SUCCESS,
                 status=http_status.HTTP_200_OK, by_alias=True, **kwargs):
        # 调用 model_dump 时，把 by_alias 传入 kwargs
        api_response = ApiResponse(code=code, data=data, message=message)
        content = api_response.model_dump(by_alias=by_alias)
        super().__init__(content=content, status_code=status)


class ErrorResponse(Response):
    """
    失败响应
    """

    def __init__(self, message=None, code=http.HTTP_ERROR, status=http_status.HTTP_200_OK):
        super().__init__(content=ApiResponse(code=code, message=message).model_dump(), status_code=status)

