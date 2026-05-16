from sqlalchemy import select

from app.db.models import Profile
from app.db.session import LocalSession
from app.schemas.profile import ProfileCreateSchema, ProfileUpdateSchema


async def add_profile(data: ProfileCreateSchema, user_id: int) -> Profile:
     async with LocalSession() as session:
        stmt = (
            Profile(user_id = user_id,
                    title = data.title,
                    description = data.description,
                    tags = data.tags
            )
        )
        session.add(stmt)
        await session.commit()
        await session.refresh(stmt)
        return stmt

async def update_profile(data: ProfileUpdateSchema) -> Profile:
    async with LocalSession() as session:
        stmt = (
            select(Profile)
            .where(Profile.id == data.id)
        )
        result = await session.execute(stmt)
        profile = result.scalar_one_or_none()
        if profile:
            profile.title = data.title
            profile.description = data.description
            profile.tags = data.tags
        await session.commit()
        return profile


async def get_profiles(user_id: int) -> list[Profile]:
    async with LocalSession() as session:
        stmt = (
            select(Profile)
            .where(Profile.user_id == user_id)
        )
        result = await session.execute(stmt)
        profiles = result.scalars().all()
        return profiles


async def get_user_profile(profile_id: int) -> Profile:
    async with LocalSession() as session:
        stmt = (
            select(Profile)
            .where(Profile.id == profile_id)
        )
        result = await session.execute(stmt)
        profile = result.scalar_one_or_none()
        return profile