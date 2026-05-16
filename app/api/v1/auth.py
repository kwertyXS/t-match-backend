import logging

import jwt
from fastapi import APIRouter, Depends, Security, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPBearer, HTTPAuthorizationCredentials

from app.db.models import User
from app.repository.auth import get_user_by_login
from app.schemas.auth import RegistrationSchema, LoginSchema
from app.services.auth import registration, get_user, login, refresh
from app.validators.password import get_current_user
from settings import settings

router = APIRouter()
security = HTTPBearer()

@router.post("/registration")
async def register(data: RegistrationSchema):
    """Регистрация пользователя"""
    return await registration(data)

@router.post("/login")
async def login_user(data: LoginSchema):
    """Вход пользователя в УЗ"""
    return await login(data)

@router.get("/user/{login}")
async def get_user_by_login(login: str):
    """Получение пользователя по логину"""
    return await get_user(login)

@router.get("/health")
async def health():
    return {"status": "ok"}

@router.get("/me")
async def read_users_me(current_user: dict = Depends(get_current_user)):
    """Получение пользователя по токену"""
    user = await get_user_by_login(current_user['login'])

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": user.id,
        "login": user.nickname,
        "email": user.email,
        "tg": user.telegram
    }
@router.post("/refresh")
async def refresh_token(token: str):
    """Получение access токена"""
    return await refresh(token)