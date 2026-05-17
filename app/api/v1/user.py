from fastapi import APIRouter, Depends, HTTPException

from app.schemas.user import UserSchema, UserResponseSchema
from app.services.auth import get_user
from app.services.user import edit_user, get_owner_profile, find_user, get_user_by_token
from app.validators.password import get_current_user

router = APIRouter()

@router.get("/user/{id}")
async def get_user_by_id(id: int) -> UserResponseSchema:
    """Получение пользователя по id"""
    return await find_user(id)

@router.get("/user/{login}")
async def get_user_by_login(login: str) -> UserResponseSchema:
    """Получение пользователя по логину"""
    return await get_user(login)


@router.get("/user/{profile}")
async def get_user_by_profile(profile_id: int) -> UserResponseSchema:
    """Получение юзера по профилю"""
    return await get_owner_profile(profile_id)

@router.get("/me")
async def get_users_me(current_user: dict = Depends(get_current_user))  -> UserResponseSchema:
    """Получение пользователя по токену"""
    return await get_user_by_token(current_user)

@router.patch("/user")
async def update_user(data: UserSchema, current_user: dict = Depends(get_current_user)) -> UserResponseSchema:
    """изменение юзера"""
    return await edit_user(data)
