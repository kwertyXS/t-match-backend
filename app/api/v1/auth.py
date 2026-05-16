from fastapi import APIRouter, Depends, Security, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.db.models import User
from app.repository.auth import get_user_by_login
from app.schemas.auth import Registration, Login
from app.services.auth import registration, get_user, login
from app.validators.password import get_current_user

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/login")

@router.post("/registration")
async def register(data: Registration):
    return await registration(data)

@router.post("/login")
async def register(data: OAuth2PasswordRequestForm = Depends()):
    return await login(data)

@router.get("/user/{login}")
async def get_user_by_id(login: str):
    return await get_user(login)

@router.get("/health")
async def health():
    return {"status": "ok"}


@router.get("/me")
async def read_users_me(current_user: dict = Depends(get_current_user)):
    user = await get_user_by_login(current_user['login'])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
            "id": user.id,
            "login": user.nickname,
            "email": user.email,
            "tg": user.telegram
        }

