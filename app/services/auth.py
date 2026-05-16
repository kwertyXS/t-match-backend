import datetime

import jwt
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_jwt import JwtAccessBearer
from sqlalchemy.util import await_only

from app.db.session import AsyncSession

from app.schemas.auth import RegistrationSchema, LoginSchema

from app.repository.auth import add_user, is_user_exists, get_user_by_login, get_refresh_token, update_refresh_token, \
    is_tg_exists, is_email_exists
from app.validators.password import verify_password, create_refresh_token, create_access_token
from settings import settings

access_security = JwtAccessBearer(secret_key=settings.SECRET_KEY)

async def registration(data: RegistrationSchema):
    if await is_user_exists(data.login):
        raise HTTPException(status_code=400, detail="User already exists")

    if data.telegram:
        if await is_tg_exists(data.telegram):
            raise HTTPException(status_code=400, detail="Telegram already exists")

    if data.email:
        if await is_email_exists(data.email):
            raise HTTPException(status_code=400, detail="Email already exists")

    refresh_token_expires = datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token = create_refresh_token(
        data={"sub": data.login}, expires_delta=refresh_token_expires
    )

    user = await add_user(data, refresh_token)

    if user is not None:
        return {"refresh_token": refresh_token}
    else:
        return {"ok": False}

async def get_user(login: str):
    user = await get_user_by_login(login)
    if user:
        return {"id": user.id, "login": user.nickname, "email": user.email, "tg": user.telegram}
    else:
        raise HTTPException(status_code=400, detail="User does not exist")


async def login(data: LoginSchema) -> dict[str, str]:
    user = await get_user_by_login(data.login)
    if await verify_password(data.password, user.password_hash):
        refresh_token_expires = datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token = create_refresh_token(
        data={"sub": user.nickname}, expires_delta=refresh_token_expires
        )
        await update_refresh_token(user.nickname, refresh_token)
        return {
          "refresh_token": refresh_token,
          "token_type": "bearer"
        }

    else:
        raise HTTPException(status_code=400, detail="Incorrect password")


async def refresh(refresh_token) -> dict[str, str]:
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")

    try:
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM],
                             options={"verify_exp": False})
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token payload")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    try:
        jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except Exception:
        raise HTTPException(status_code=401, detail="Token expired")


    user = await get_user_by_login(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_access_token = create_access_token(data={"sub": user.nickname})


    return {"access_token": new_access_token, "token_type": "bearer"}