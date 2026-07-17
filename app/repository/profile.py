from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Profile
from app.schemas.profile import ProfileCreateSchema, ProfileUpdateSchema


async def add_profile(
    session: AsyncSession, data: ProfileCreateSchema, user_id: int
) -> Profile:
    stmt = Profile(
        user_id=user_id, title=data.title, description=data.description, tags=data.tags
    )
    session.add(stmt)
    await session.commit()
    await session.refresh(stmt)
    return stmt


async def update_profile(session: AsyncSession, data: ProfileUpdateSchema) -> Profile:
    stmt = select(Profile).where(Profile.id == data.id)
    result = await session.execute(stmt)
    profile = result.scalar_one_or_none()
    if profile:
        profile.title = data.title
        profile.description = data.description
        profile.tags = data.tags
    await session.commit()
    return profile


async def get_profiles(session: AsyncSession, user_id: int) -> list[Profile]:
    stmt = select(Profile).where(Profile.user_id == user_id)
    result = await session.execute(stmt)
    profiles = result.scalars().all()
    return profiles


async def get_user_profile(session: AsyncSession, profile_id: int) -> Profile:
    stmt = select(Profile).where(Profile.id == profile_id)
    result = await session.execute(stmt)
    profile = result.scalar_one_or_none()
    return profile


async def get_profile_by_id(session: AsyncSession, profile_id) -> Profile:
    stmt = select(Profile).where(Profile.id == profile_id)
    result = await session.execute(stmt)
    profile = result.scalar_one_or_none()
    return profile
