import uuid
from datetime import timedelta, datetime, timezone

from fastapi.param_functions import Body
from fastapi import Request, Depends, HTTPException, status
from pwdlib import PasswordHash
from annotated_doc import Doc
from sqlalchemy.ext.asyncio import AsyncSession

from apps.modules.sys.basis.crud.crud_sys_user import CrudSysUser
from apps.modules.sys.basis.models.sys_user import SysUserModel
from config import settings
from core.constants import auth_constant
from core.framework.crud_async_session import AsyncGenericCRUD, crud_getter
from core.framework.log_tools import logger
from core.framework.database import db_getter

from typing import Annotated, Any, List

import jwt
from jwt import InvalidTokenError, ExpiredSignatureError
from pydantic import BaseModel, Field

from config.settings import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from core.utils.JSONUtils import JSONUtils
from core.framework.sql_alchemy_helper import SQLAlchemyHelper
from core.framework.cache_tools import cache

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


class AuthValidation:

    @classmethod
    def verify_password(cls, plain_password, hashed_password):
        return password_hash.verify(plain_password, hashed_password)

    @classmethod
    def get_password_hash(cls, password):
        return password_hash.hash(password)

    @classmethod
    async def create_access_token(cls, data: Any):
        to_encode = data.copy()
        to_encode.pop('user', None)
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        # to_encode.update({"exp": expire})
        # 2. 关键修复：将datetime转换为Unix时间戳（秒数）
        to_encode.update({"exp": expire.timestamp()})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        user_dict = data.get("user").__dict__
        user_dict.pop("password")
        # redis缓存过期时间,过期时间比jwt 晚30分钟
        ex_ms = (ACCESS_TOKEN_EXPIRE_MINUTES * 60 * 1000) + 1800000
        await cache.set("auth:" + data.get("sub"), JSONUtils.dumps(user_dict), ex_ms)
        return encoded_jwt

    @classmethod
    async def validate_token(cls, token: str, ):
        print("验证token")
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
                await cache.delete("auth:" + payload.get("sub"))
            print("获取token异常")
            raise credentials_exception
        cache_user_info: str = await cache.get("auth:" + token_key)
        user = None
        if cache_user_info:
            user = JSONUtils.loads(cache_user_info)
        if user is None:
            raise credentials_exception
        return user

    def parse_token_payload(token: str) -> dict | None:
        """
        解析JWT Payload，即使token过期也能手动解析
        :param token: JWT字符串
        :return: 解析后的Payload字典，解析失败返回None
        """
        try:
            # 第一步：尝试正常解析（校验过期、签名等）
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
                print(f"手动解析过期Token失败：{e}")
                return None
        except InvalidTokenError as e:
            # 其他无效token情况（如签名错误、格式错误）
            print(f"Token无效：{e}")
            return None

    @classmethod
    async def validate_permissions(cls, permissions: set[str] | None = None, user_permissions: set[str] | None = None):
        print("验证用户权限", permissions)
        if permissions:  # 需要验证权限
            print("校验")
            if user_permissions:  # 用户是否有分配权限
                if user_permissions != {auth_constant.ALL_PERMISSION}:  # 是否管理员权限
                    if not (permissions & user_permissions):  # 用户是否拥有指定权限需要的权限
                        raise HTTPException(
                            status_code=status.HTTP_403_FORBIDDEN,
                            detail="无权限操作"
                        )
            else:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="无权限操作"
                )

    @classmethod
    async def validate_role_permissions(cls, roles: set[str] | None = None, user_roles: set[str] | None = None):
        print("验证用户角色权限", roles)
        if roles:  # 需要验证权限
            if user_roles:  # 用户是否有分配权限
                if not (roles & user_roles):  # 用户是否拥有指定权限需要的权限
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="无权限操作"
                    )
            else:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="无权限操作"
                )


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
        print("登录", login_request_param)

        user = await crud_async_session.first_model(
            "select * from tbl_sys_user where account = :account",
            {"account": login_request_param.account},
            SysUserModel
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="账号或密码错误"
            )
        if not self.verify_password(login_request_param.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="账号或密码错误"
            )
        # 这里模拟查询用户权限编码
        user_role_permissions = await CrudSysUser.get_sys_user_permission(user.id, crud_async_session)
        user.roles = user_role_permissions
        access_token = await AuthValidation.create_access_token(
            data={"sub": uuid.uuid4().hex, "user": user}
        )
        print("登录成功")
        return Token(access_token=access_token, token_type="bearer")


class AuthAuthorize(AuthValidation):
    """
    token 登录认证
    """

    async def __call__(self, request: Request,
                       token: str = Depends(settings.oauth2_scheme),
                       db: AsyncSession = Depends(db_getter)) -> Auth:
        print("进行接口登录验证")

        # token 登录认证
        user = await self.validate_token(token)
        request.state.user = user
        auth = Auth(user=user, db=db)
        return auth


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
        print("进行接口权限校验")
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
            print("验证用户权限", self.permissions)
            if permission_codes:
                # 用户权限验证
                await self.validate_permissions(self.permissions, permission_codes)
            else:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                )
        if self.roles:
            print("验证用户角色权限", self.roles)
            if role_codes:
                await self.validate_role_permissions(self.roles, role_codes)
            else:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                )
        return None
