from fastapi import APIRouter, Depends
from sqlalchemy.util import await_fallback

from app.schemas.user import UserSchema
from app.services.user import edit_user, get_owner_profile
from app.validators.password import get_current_user

router = APIRouter()

@router.patch("/user")
async def update_user(data: UserSchema, current_user: dict = Depends(get_current_user)):
    """изменение юзера"""
    return await edit_user(data)

@router.get("/user{profile}")
async def get_user_by_profile(profile_id: int):
    return await get_owner_profile(profile_id)
