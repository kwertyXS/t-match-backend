from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User, Profile
from app.schemas.user import UserSchema


async def update_user(session: AsyncSession, data: UserSchema) -> User:
    stmt = select(User).where(User.nickname == data.nickname)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    if user:
        user.email = data.email
        user.telegram = data.telegram
        await session.commit()
    return user


async def get_user_by_profile(session: AsyncSession, profile_id: int) -> User:
    stmt = (
        select(User)
        .join(Profile, Profile.user_id == User.id)
        .where(Profile.id == profile_id)
    )
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    return user


async def get_user_by_id(session: AsyncSession, user_id: int) -> User:
    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    return user


async def get_user_by_login(session: AsyncSession, login: str) -> User:
    stmt = select(User).where(User.nickname == login)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    return user
