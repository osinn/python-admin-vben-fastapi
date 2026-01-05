import uuid
from datetime import timedelta, datetime, timezone

from fastapi.param_functions import Body
from fastapi import Request, Depends, HTTPException, status
from pwdlib import PasswordHash
from annotated_doc import Doc
from sqlalchemy.ext.asyncio import AsyncSession

from apps.modules.sys.basis.models.sys_user import SysUserModel
from config import settings
from core.framework.database import db_getter

from typing import Annotated, Any

import jwt
from jwt import InvalidTokenError
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
    async def create_access_token(cls, data: Any, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        to_encode.pop('user', None)
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        user_dict = data.get("user").__dict__
        user_dict.pop("password")
        await cache.set(data.get("sub"), JSONUtils.dumps(user_dict))
        return encoded_jwt

    @classmethod
    async def validate_token(cls, token: str, permissions: set[str] | None = None):
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
                raise credentials_exception
        except InvalidTokenError:
            raise credentials_exception
        cache_user_info: str = await cache.get(token_key)
        user = None
        if cache_user_info:
            user = JSONUtils.loads(cache_user_info)
        if user is None:
            raise credentials_exception

        print("验证用户权限", permissions)
        if permissions:
            print("校验")
            # 用户权限验证
            user_permissions = user.get("permissions")
            await cls.validate_permissions(permissions, set(user_permissions) if user_permissions else None )
        return user

    @classmethod
    async def validate_permissions(cls, permissions: set[str] | None = None, user_permissions: set[str] | None = None):
        print("验证用户权限", permissions)
        if permissions: # 需要验证权限
            print("校验")
            if user_permissions: # 用户是否有分配权限
                if user_permissions != {'*.*.*'}: # 是否管理员权限
                    if not (permissions & user_permissions): # 用户是否拥有指定权限需要的权限
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
                       db: AsyncSession = Depends(db_getter)) -> Token:
        print("登录", login_request_param)

        user = await SQLAlchemyHelper.execute_first_model(db, SysUserModel,
                                                          "select * from tbl_sys_user where account = :account",
                                                          {"account": login_request_param.account}
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
        user_permissions = set()
        user_permissions.add("sys.user.list")
        user.permissions = user_permissions
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = await AuthValidation.create_access_token(
            data={"sub": uuid.uuid4().hex, "user": user}, expires_delta=access_token_expires
        )
        print("登录成功")
        return Token(access_token=access_token, token_type="bearer")

class AuthAuthorize(AuthValidation):
    """
    1、token 登录认证
    2、用户 权限验证
    """

    def __init__(self, permissions: list[str] | None = None):
        print("接口需要的权限")
        if permissions:
            self.permissions = set(permissions)
        else:
            self.permissions = None

    async def __call__(self, request: Request,
                       token: str = Depends(settings.oauth2_scheme),
                       db: AsyncSession = Depends(db_getter)) -> Auth:
        print("进行接口权限校验")

        # token 登录认证
        user = await self.validate_token(token, self.permissions)

        auth = Auth(user=user, db=db)
        return auth
