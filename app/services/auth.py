import datetime

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_jwt import JwtAccessBearer

from app.db.session import AsyncSession

from app.schemas.auth import Registration, Login

from app.repository.auth import add_user, is_user_exists, get_user_by_login
from app.validators.password import verify_password, create_refresh_token
from settings import settings


async def registration(data: Registration):
    if await is_user_exists(data.login):
        raise HTTPException(status_code=400, detail="User already exists")
    user = await add_user(data)
    if user is not None:
        return {"id": user.id, "login": user.nickname}
    else:
        return {"ok": False}

async def get_user(login: str):
    user = await get_user_by_login(login)
    if user:
        return {"id": user.id, "login": user.nickname, "email": user.email, "tg": user.telegram}
    else:
        raise HTTPException(status_code=400, detail="User does not exist")

access_security = JwtAccessBearer(secret_key=settings.SECRET_KEY)

async def login(data: OAuth2PasswordRequestForm = Depends()) -> dict[str, str]:
    user = await get_user_by_login(data.username)
    if await verify_password(data.password, user.password_hash):
    #     return {"access_token" :access_security.create_access_token(subject={"id": user.id, "login": user.nickname})}
        refresh_token_expires = datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token = create_refresh_token(
        data={"sub": user.login}, expires_delta=refresh_token_expires
        )
        return {
          "refresh_token": refresh_token,
          "token_type": "bearer"
        }

    else:
        raise HTTPException(status_code=400, detail="Incorrect password")
