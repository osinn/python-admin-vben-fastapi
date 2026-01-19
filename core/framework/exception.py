from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
from starlette import status
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI
from core.framework.log_tools import logger
from config.settings import DEBUG


class BizException(Exception):

    def __init__(
            self,
            msg: str,
            code: int = status.HTTP_400_BAD_REQUEST,
            status_code: int = status.HTTP_200_OK,
            desc: str = None,
            error: str = None
    ):
        self.msg = msg
        self.code = code
        self.status_code = status_code
        self.desc = desc
        self.error = error
class SqlException(Exception):

    def __init__(
            self,
            msg: str,
            code: int = status.HTTP_400_BAD_REQUEST,
            status_code: int = status.HTTP_200_OK,
            desc: str = None,
            error: str = None
    ):
        self.msg = msg
        self.code = code
        self.status_code = status_code
        self.desc = desc
        self.error = error


def register_exception(app: FastAPI):
    """
    异常捕捉
    """

    @app.exception_handler(BizException)
    async def custom_exception_handler(request: Request, exc: BizException):
        """
        自定义异常
        """
        if DEBUG:
            print("请求地址", request.url.__str__())
            print("捕捉到重写BizException异常异常：biz_exception_handler")
            print(exc.desc)
            print(exc.msg)
        # 打印栈信息，方便追踪排查异常
        logger.exception(exc)
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": exc.msg, "code": exc.code, "exc_error": exc.error},
        )

    @app.exception_handler(StarletteHTTPException)
    async def unicorn_exception_handler(request: Request, exc: StarletteHTTPException):
        """
        重写HTTPException异常处理器
        """
        if DEBUG:
            print("请求地址", request.url.__str__())
            print("捕捉到重写HTTPException异常异常：unicorn_exception_handler")
            print(exc.detail)
        # 打印栈信息，方便追踪排查异常
        logger.exception(exc)
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "code": exc.status_code,
                "message": exc.detail,
            }
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        # # 遍历错误信息，替换提示
        # error_details = []
        # for error in exc.errors():
        #     loc = error["loc"]
        #     msg = error["msg"]
        #     # 替换 field required 提示
        #     if msg == "Field required":
        #         field_name = loc[-1] if loc else "未知字段"
        #         msg = f"字段 {field_name} 为必填项"
        #     error_details.append({"field": loc, "message": msg})
        #
        # return JSONResponse(
        #     status_code=422,
        #     content={
        #         "status": "error",
        #         "message": "参数验证失败",
        #         "errors": error_details
        #     }
        # )
        """
        重写请求验证异常处理器
        """
        if DEBUG:
            print("请求地址", request.url.__str__())
            print("捕捉到重写请求验证异常异常：validation_exception_handler")
            print(exc.errors())
        # 打印栈信息，方便追踪排查异常
        logger.exception(exc)
        error = exc.errors()[0]
        msg = exc.errors()[0].get("msg")
        # msg = "请求失败，缺少必填项！"
        loc = error["loc"]
        # 替换 field required 提示
        field_name = loc[-1] if loc else "未知字段"
        if msg == "field required" or msg == "Field required":
            msg = f"字段 {field_name} 为必填项"
        elif msg == "value is not a valid list":
            print(exc.errors())
            msg = f"{field_name}参数应该为集合！"
        elif msg == "value is not a valid int":
            msg = f"{field_name}参数应该为整数！"
        elif msg == "value could not be parsed to a boolean":
            msg = f"{field_name}参数应该为布尔值！"
        elif msg == "Input should be a valid list":
            msg = f"{field_name}应该是一个有效的集合！"
        return JSONResponse(
            status_code=200,
            content=jsonable_encoder(
                {
                    "message": msg,
                    "body": exc.body,
                    "code": status.HTTP_400_BAD_REQUEST
                }
            ),
        )

    @app.exception_handler(ValueError)
    async def value_exception_handler(request: Request, exc: ValueError):
        """
        捕获值异常
        """
        if DEBUG:
            print("请求地址", request.url.__str__())
            print("捕捉到值异常：value_exception_handler")
            print(exc.__str__())
        # 打印栈信息，方便追踪排查异常
        logger.exception(exc)
        return JSONResponse(
            status_code=200,
            content=jsonable_encoder(
                {
                    "message": exc.__str__(),
                    "code": status.HTTP_400_BAD_REQUEST
                }
            ),
        )

    @app.exception_handler(Exception)
    async def all_exception_handler(request: Request, exc: Exception):
        """
        捕获全部异常
        """
        if DEBUG:
            print("请求地址", request.url.__str__())
            print("捕捉到全局异常：all_exception_handler")
            print(exc.__str__())
        # 打印栈信息，方便追踪排查异常
        logger.exception(exc)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=jsonable_encoder(
                {
                    "message": "接口异常！",
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "error": exc.__str__(),
                }
            ),
        )


#
# # 自定义全局异常处理
# @app.exception_handler(Exception)
# async def custom_exception_handler(request: Request, exc: Exception):
#     # 区分是业务异常（手动抛的）还是系统异常
#     if str(exc) == "演示异常":  # 匹配自定义异常信息
#         return JSONResponse(
#             status_code=200,  # 业务异常可返回200，用code区分
#             content=jsonable_encoder(ErrorResponse(
#                 code=10001,  # 自定义业务错误码
#                 msg=str(exc),  # 异常信息
#             ))
#         )
#     # 其他系统异常（如代码bug）返回500
#     return JSONResponse(
#         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#         content=jsonable_encoder(ErrorResponse(
#             code=500,
#             msg=f"服务器内部错误：{str(exc)}",
#         ))
#     )
#
# # 4. 自定义全局校验异常 RequestValidationError 异常处理器
# @app.exception_handler(RequestValidationError)
# async def custom_validation_exception_handler(
#         request: Request, exc: RequestValidationError
# ):
#     # 1. 解析原始错误信息（Pydantic 抛出的错误）
#     raw_errors = exc.errors()
#     error_details = {}
#     error = None
#
#     # 2. 格式化错误详情（按字段分类）
#     for err in raw_errors:
#         field = ".".join(map(str, err["loc"][1:]))  # 提取字段名（跳过 body 层级）
#         msg = err["msg"]
#         e: ValueError = err.get('ctx').get('error')
#         # error_details[field] = str(e) # 或 e.args[0]
#         error = str(e) # 或 e.args[0]
#
#     # 3. 构造自定义响应内容
#     response_data = ErrorResponse(
#         code=status.HTTP_422_UNPROCESSABLE_ENTITY,  # 422 是默认的校验错误码
#         msg=error
#     )
#
#     # 4. 返回 JSON 响应
#     return JSONResponse(
#         status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#         content=jsonable_encoder(response_data.dict())
#     )