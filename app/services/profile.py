from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.user import get_user_by_login
from app.repository.profile import (
    add_profile,
    update_profile,
    get_profiles,
    get_user_profile,
)
from app.schemas.profile import ProfileCreateSchema, ProfileUpdateSchema
from app.validators.password import get_current_user


async def get_profile(session: AsyncSession, profile_id: int):
    profile = await get_user_profile(session, profile_id)
    return {
        "id": profile.id,
        "user_id": profile.user_id,
        "title": profile.title,
        "description": profile.description,
        "tags": profile.tags,
    }


async def get_user_profiles(
    session: AsyncSession, current_user: dict = Depends(get_current_user)
):
    user = await get_user_by_login(session, current_user["login"])
    profiles = await get_profiles(session, user.id)
    return profiles


async def new_profile(
    session: AsyncSession,
    data: ProfileCreateSchema,
    current_user: dict = Depends(get_current_user),
):
    user = await get_user_by_login(session, current_user["login"])
    prof = await add_profile(session, data, user.id)
    if prof is not None:
        return {
            "id": prof.id,
            "title": prof.title,
            "description": prof.description,
            "tags": prof.tags,
        }
    else:
        return {"ok": False}


async def edit_profile(session: AsyncSession, data: ProfileUpdateSchema):
    profile = await update_profile(session, data)
    return {
        "title": profile.title,
        "description": profile.description,
        "tags": profile.tags,
    }
