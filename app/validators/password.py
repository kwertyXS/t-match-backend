import asyncio
import datetime
from typing import Optional

from fastapi import Depends, HTTPException
import jwt
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette import status

from settings import settings

import bcrypt

security = HTTPBearer()


async def hash_password(password: str, rounds: int = 12) -> str:
    def _hash():
        salt = bcrypt.gensalt(rounds=rounds)
        hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed.decode("utf-8")

    hashed_password = await asyncio.to_thread(_hash)
    return hashed_password


async def verify_password(password: str, hashed_password: str) -> bool:
    def _verify():
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))

    return await asyncio.to_thread(_verify)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + datetime.timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(
    data: dict, expires_delta: Optional[datetime.timedelta] = None
) -> str:
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + datetime.timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )
    print(f"DEBUG: REFRESH_TOKEN_EXPIRE_DAYS = {settings.REFRESH_TOKEN_EXPIRE_DAYS}")
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """Это ЗАВИСИМОСТЬ, а не эндпоинт!"""
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        login: str = payload.get("sub")

        if login is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return {"login": login}

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
