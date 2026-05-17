from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer

from app.schemas.auth import RegistrationSchema, LoginSchema
from app.services.auth import registration, login, refresh

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


@router.get("/health")
async def health():
    return {"status": "ok"}


@router.post("/refresh")
async def refresh_token(token: str):
    """Получение access токена"""
    return await refresh(token)