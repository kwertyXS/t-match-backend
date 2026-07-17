from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.services.profile import (
    new_profile,
    edit_profile,
    get_user_profiles,
    get_profile,
)
from app.schemas.profile import (
    ProfileCreateSchema,
    ProfileUpdateSchema,
    ResponseProfileSchema,
)
from app.validators.password import get_current_user

router = APIRouter()


@router.get("/profile/{id}")
async def get_user_profile(
    id: int, db: AsyncSession = Depends(get_db)
) -> ResponseProfileSchema:
    return await get_profile(db, id)


@router.get("/profiles")
async def get_profiles(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return await get_user_profiles(db, current_user)


@router.post("/profile")
async def profile(
    data: ProfileCreateSchema,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return await new_profile(db, data, current_user)


@router.patch("/profile")
async def update_profile(
    data: ProfileUpdateSchema,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return await edit_profile(db, data)
