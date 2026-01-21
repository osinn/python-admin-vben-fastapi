import time
import uuid
from datetime import timedelta, datetime, timezone

from fastapi.param_functions import Body
from fastapi import Request, Depends, HTTPException, status
from pwdlib import PasswordHash
from sqlalchemy.ext.asyncio import AsyncSession

from apps.modules.sys.basis.crud.crud_sys_user import CrudSysUser
from apps.modules.sys.basis.models.sys_user import SysUserModel
from apps.modules.sys.basis.schemas.sys_user import SysUserSchema
from apps.modules.sys.monitor.crud.crud_sys_http_log import CrudSysHttpLog
from apps.modules.sys.monitor.models.sys_http_log import SysHttpLogModel
from config import settings
from core.constants import auth_constant
from core.constants.auth_constant import SUPER_ADMIN_ROLE, CACHE_OFFLINE_PREFIX
from core.framework.crud_async_session import AsyncGenericCRUD, crud_getter
from core.framework.exception import BizException
from core.framework.log_tools import logger
from core.framework.database import db_getter

from typing import Any, Optional

import jwt
from jwt import InvalidTokenError, ExpiredSignatureError
from pydantic import BaseModel, Field

from config.settings import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from core.utils.JSONUtils import JSONUtils
from core.framework.cache_tools import cache
from core.utils.ModelUtils import ModelUtils
from core.utils.ip_utils_ip2region import ip_location_service
from core.utils.rsa_utils import decrypt_with_private_b64
from core.utils.web_request_utils import WebRequestUtils

password_hash = PasswordHash.recommended()


class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        # 接收任意类型
        arbitrary_types_allowed = True


class LoginRequestParam(BaseModel):
    account: str = Field(
        ...,
        description="`account` 登录账号",
        examples=["user123"]
    )
    password: str = Field(
        ...,
        description="`password` 登录密码",
        json_schema_extra={"format": "password"},
        examples=["secret123"]
    )
    ticket: str = Field(
        ...,
        description="票据",
        examples=["ticket123"]
    )


async def deleted_online_user(sub: str):
    """
    移除用户登录信息
    :param sub:
    :return:
    """
    await cache.delete(CACHE_OFFLINE_PREFIX + sub)


async def fetch_online_user_all():
    """
    拉取所以在线用户信息
    :return:
    """
    online_user_all = await cache.fetch_like(CACHE_OFFLINE_PREFIX + "*")
    return online_user_all


async def get_online_user(sub: str) -> Optional[dict]:
    """
    获取缓存在线用户信息
    :param sub: 登录时分配的sub
    :return:
    """
    online_user = await cache.get(CACHE_OFFLINE_PREFIX + sub)
    if online_user:
        return JSONUtils.loads(online_user)
    else:
        return None


class AuthValidation:

    @classmethod
    def verify_password(cls, plain_password, hashed_password):
        return password_hash.verify(plain_password, hashed_password)

    @classmethod
    def get_password_hash(cls, password):
        return password_hash.hash(password)

    @classmethod
    async def save_online_user(cls, sub: str, user: dict):
        # redis缓存过期时间,过期时间比jwt 晚30分钟
        ex_ms = (ACCESS_TOKEN_EXPIRE_MINUTES * 60 * 1000) + 1800000
        await cache.set(CACHE_OFFLINE_PREFIX + sub, JSONUtils.dumps(user), ex_ms)

    @classmethod
    async def create_access_token(cls, data: Any):
        to_encode = data.copy()
        to_encode.pop('user', None)
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire.timestamp()})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        user_dict = data.get("user")
        is_admin = cls.hash_admin(user_dict)
        user_dict["is_admin"] = is_admin
        user_dict["sub"] = data["sub"]
        user_dict["login_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        await cls.save_online_user(data.get("sub"), user_dict)
        return encoded_jwt

    @classmethod
    async def validate_token(cls, token: str, ):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="登录超时，请重新登录",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            token_key = payload.get("sub")
            if token_key is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="无效的登录凭证",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        except Exception:
            payload = cls.parse_token_payload(token)
            if payload:
                # 删除缓存数据
                await cache.delete(CACHE_OFFLINE_PREFIX + payload.get("sub"))
            raise credentials_exception
        cache_user_info: str = await cache.get(CACHE_OFFLINE_PREFIX + token_key)
        user = None
        if cache_user_info:
            user = JSONUtils.loads(cache_user_info)
        if user is None:
            raise credentials_exception
        user["sub"] = payload.get("sub")
        return user

    def parse_token_payload(token: str) -> dict | None:
        """
        解析JWT Payload，即使token过期也能手动解析
        :param token: JWT字符串
        :return: 解析后的Payload字典，解析失败返回None
        """
        try:
            return jwt.decode(
                token,
                SECRET_KEY,
                algorithms=[ALGORITHM]
            )
        except ExpiredSignatureError:
            try:
                payload = jwt.decode(
                    token,
                    SECRET_KEY,
                    algorithms=[ALGORITHM],
                    options={"verify_exp": False}  # 手动关闭过期校验
                )
                return payload
            except InvalidTokenError as e:
                logger.error(f"手动解析过期Token失败：{e}")
                return None
        except InvalidTokenError as e:
            # 其他无效token情况（如签名错误、格式错误）
            logger.error(f"Token无效：{e}")
            return None

    @classmethod
    async def validate_permissions(cls, permissions: set[str] | None = None, user_permissions: set[str] | None = None):
        if permissions:  # 需要验证权限
            if user_permissions:  # 用户是否有分配权限
                if user_permissions != {auth_constant.ALL_PERMISSION}:  # 是否管理员权限
                    if not (permissions & user_permissions):  # 用户是否拥有指定权限需要的权限
                        raise BizException(
                            "无权限操作",
                            code=status.HTTP_403_FORBIDDEN
                        )
            else:
                raise BizException(
                    "无权限操作",
                    code=status.HTTP_403_FORBIDDEN
                )

    @classmethod
    async def validate_role_permissions(cls, roles: set[str] | None = None, user_roles: set[str] | None = None):
        if roles:  # 需要验证权限
            if user_roles:  # 用户是否有分配权限
                if not (roles & user_roles):  # 用户是否拥有指定权限需要的权限
                    raise BizException(
                        "无权限操作",
                        code=status.HTTP_403_FORBIDDEN
                    )
            else:
                raise BizException(
                    "无权限操作",
                    code=status.HTTP_403_FORBIDDEN
                )

    @classmethod
    def hash_admin(self, user: dict) -> bool:
        """
        检查在线用户是否是管理员角色
        :param user: 在线用户信息
        :return:
        """
        roles = user.get("roles", None)
        if roles is None:
            return False
        for role in roles:
            if role["role_code"] == SUPER_ADMIN_ROLE:
                return True
        return False


class Auth(BaseModel):
    user: Any = None
    db: AsyncSession = Depends(db_getter)
    data_range: int | None = None
    dept_ids: list | None = []

    class Config:
        # 接收任意类型
        arbitrary_types_allowed = True


class LoginAuth(AuthValidation):

    async def __call__(self, request: Request,
                       login_request_param: LoginRequestParam = Body(),
                       crud_async_session: AsyncGenericCRUD = Depends(crud_getter(SysUserModel))) -> Token:
        start_time = time.time()
        ip = WebRequestUtils.get_client_ip(request)
        browser_info = WebRequestUtils.get_browser_info(request)
        sys_http_log = SysHttpLogModel(
            account=login_request_param.account,
            ip_address=ip,
            request_uri=request.url.path,
            request_method=request.method,
            business_module="用户登录",
            module_name="用户登录",
            source="WEB",
            log_type="LOGIN",
            action_desc="用户登录",
            operate_type="用户登录",
            browser=browser_info.get("browser_name", None),
            os=browser_info.get("os_name", None),
            mobile=browser_info.get("is_mobile", False),
            ip_address_attr=ip_location_service.get_ip_address_attr(ip)
        )
        try:
            user = await crud_async_session.first_model(
                # 未删除、未锁账号、启用状态
                "select * from tbl_sys_user where is_deleted = 0 and lock_account = 1 and status = 1 and account = :account",
                {"account": login_request_param.account},
                SysUserSchema
            )
            if not user:
                raise BizException(
                    "账号或密码错误",
                    code=status.HTTP_401_UNAUTHORIZED
                )
            private_key = await cache.get("rsa:private:" + login_request_param.ticket)
            password = decrypt_with_private_b64(login_request_param.password, private_key)
            if not self.verify_password(password, user.password):
                raise BizException(
                    "账号或密码错误",
                    code=status.HTTP_401_UNAUTHORIZED
                )
            user_role_permissions = await CrudSysUser.get_sys_user_permission(user.id, crud_async_session)
            user.roles = user_role_permissions

            user_dict = ModelUtils.to_dict(user)

            user_dict["browser"] = browser_info["browser_name"]
            user_dict["operating_system"] = browser_info["os_name"]
            user_dict["ip"] = ip

            access_token = await AuthValidation.create_access_token(data={"sub": uuid.uuid4().hex, "user": user_dict})
            sys_http_log.status = 1
            return Token(access_token=access_token, token_type="bearer")
        except Exception as e:
            sys_http_log.status = 2
            sys_http_log.exception_msg = f"{e}"
            logger.error(f"登录异常：{e}")
            raise BizException("登录失败，请联系管理员", code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            end_time = time.time()
            seconds = end_time - start_time
            minutes = int(seconds // 60)
            remaining_seconds = seconds % 60
            decimal_places = 2
            format_str = f"{{}}:{{:0{decimal_places + 2}.{decimal_places}f}}"
            min_sec_str = format_str.format(minutes, remaining_seconds)
            sys_http_log.execution_time = min_sec_str
            await CrudSysHttpLog.create_login_log(sys_http_log, crud_async_session)

class AuthAuthorize(AuthValidation):
    """
    token 登录认证
    """

    async def __call__(self, request: Request,
                       token: str = Depends(settings.oauth2_scheme),
                       # db: AsyncSession = Depends(db_getter)
                       ):
        # token 登录认证
        user = await self.validate_token(token)
        request.state.user = user
        # auth = Auth(user=user, db=db)
        return user


class PreAuthorize(AuthValidation):
    """
    验证权限
    """

    def __init__(self, permissions: list[str] | None = None, roles: list[str] | None = None):
        if permissions:
            self.permissions = set(permissions)
        else:
            self.permissions = None
        if roles:
            self.roles = set(roles)
        else:
            self.roles = None

    async def __call__(self, request: Request) -> None:
        if self.roles is None and self.permissions is None:
            return None

        user = getattr(request.state, "user", None)

        roles = user.get("roles", None)
        if roles is None:
            logger.error("权限认证-用户不存在")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
        # 初始化空集合（自动去重）
        permission_codes = set()
        role_codes = set()
        # 遍历每个角色
        for role in roles:
            role_codes.add(role["role_code"])
            if "permissions" not in role or not isinstance(role["permissions"], list):
                continue
            # 遍历该角色的所有权限
            for perm in role["permissions"]:
                if "permission_code" in perm and perm["permission_code"] is not None:
                    permission_codes.add(perm["permission_code"])
        if self.permissions:
            if permission_codes:
                # 用户权限验证
                await self.validate_permissions(self.permissions, permission_codes)
            else:
                raise BizException(
                    "无权限操作",
                    code=status.HTTP_401_UNAUTHORIZED
                )
        if self.roles:
            print("验证用户角色权限", self.roles)
            if role_codes:
                await self.validate_role_permissions(self.roles, role_codes)
            else:
                raise BizException(
                    "无权限操作",
                    code=status.HTTP_401_UNAUTHORIZED
                )
        return None
