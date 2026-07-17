from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.user import UserSchema, UserResponseSchema
from app.services.auth import get_user
from app.services.user import edit_user, get_owner_profile, find_user, get_user_by_token
from app.validators.password import get_current_user

router = APIRouter()


@router.get("/user/{id}")
async def get_user_by_id(
    id: int, db: AsyncSession = Depends(get_db)
) -> UserResponseSchema:
    return await find_user(db, id)


@router.get("/user/{login}")
async def get_user_by_login(
    login: str, db: AsyncSession = Depends(get_db)
) -> UserResponseSchema:
    return await get_user(db, login)


@router.get("/user/{profile}")
async def get_user_by_profile(
    profile_id: int, db: AsyncSession = Depends(get_db)
) -> UserResponseSchema:
    return await get_owner_profile(db, profile_id)


@router.get("/me")
async def get_users_me(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
) -> UserResponseSchema:
    return await get_user_by_token(db, current_user)


@router.patch("/user")
async def update_user(
    data: UserSchema,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
) -> UserResponseSchema:
    return await edit_user(db, data)
