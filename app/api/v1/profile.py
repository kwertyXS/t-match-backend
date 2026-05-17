from fastapi import APIRouter, Depends

from app.db.models import Profile
from app.services.profile import new_profile, edit_profile, get_user_profiles, get_profile
from app.schemas.profile import ProfileCreateSchema, ProfileUpdateSchema, ResponseProfileSchema
from app.validators.password import get_current_user

router = APIRouter()

@router.get("/profile/{id}")
async def get_user_profile(profile_id: int) -> ResponseProfileSchema:
    """Получение профиля по id"""
    return await get_profile(profile_id)

@router.get("/profiles")
async def get_profiles(current_user: dict = Depends(get_current_user)):
    """Получение всех профилей пользователя"""
    return await get_user_profiles(current_user)

@router.post("/profile")
async def profile(data: ProfileCreateSchema,
                  current_user: dict = Depends(get_current_user)):
    """Создание профиля"""
    return await new_profile(data, current_user)

@router.patch("/profile")
async def update_profile(data: ProfileUpdateSchema,
                         current_user: dict = Depends(get_current_user)):
    """Изменение профиля"""
    return await edit_profile(data)
