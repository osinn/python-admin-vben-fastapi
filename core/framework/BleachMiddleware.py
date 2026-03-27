import bleach
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from pydantic import BaseModel, model_validator
from typing import Any

class BleachMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        original_path = request.url.path
        clean_path = bleach.clean(original_path)
        request.state.clean_path = clean_path

        # --- 清洗 Query 参数 (核心修改) ---
        if request.query_params:
            query_string = request.scope.get("query_string", b"").decode("utf-8")

            if query_string:
                params = dict(param.split("=", 1) for param in query_string.split("&") if "=" in param)

                clean_params = {}
                for key, value in params.items():
                    from urllib.parse import unquote, quote
                    decoded_value = unquote(value)
                    cleaned_value = bleach.clean(decoded_value)

                    clean_params[key] = quote(cleaned_value)

                new_query_string = "&".join(f"{k}={v}" for k, v in clean_params.items())

                request.scope["query_string"] = new_query_string.encode("utf-8")
        response = await call_next(request)
        return response


class CleanedBaseModel(BaseModel):
    """
    Pydantic 模型继承此类 自动清洗所有字符串类型的字段。
    """

    @model_validator(mode='before')
    @classmethod
    def clean_all_strings(cls, data: Any) -> Any:
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, str):
                    data[key] = bleach.clean(value)
                elif isinstance(value, list):
                    data[key] = [bleach.clean(v) if isinstance(v, str) else v for v in value]
        return data