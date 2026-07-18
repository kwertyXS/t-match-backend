from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.auth import RegistrationSchema, LoginSchema
from app.services.auth import registration, login, refresh

router = APIRouter()
security = HTTPBearer()


@router.post("/registration")
async def register(data: RegistrationSchema, db: AsyncSession = Depends(get_db)):
    return await registration(db, data)


@router.post("/login")
async def login_user(data: LoginSchema, db: AsyncSession = Depends(get_db)):
    return await login(db, data)


@router.post("/refresh")
async def refresh_token(token: str, db: AsyncSession = Depends(get_db)):
    return await refresh(db, token)
