from sqlalchemy import select

from app.db.models import User, Profile
from app.db.session import LocalSession
from app.schemas.user import UserSchema


async def update_user(data: UserSchema) -> User:
    async with LocalSession() as session:
        stmt = (
            select(User)
            .where(User.nickname == data.nickname)
        )
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()
        if user:
            user.email = data.email
            user.telegram = data.telegram
            await session.commit()
        return user


async def get_user_by_profile(profile_id: int) -> User:
    async with LocalSession() as session:
        # Вариант 1: Через JOIN (более эффективно)
        stmt = (
            select(User)
            .join(Profile, Profile.user_id == User.id)
            .where(Profile.id == profile_id)
        )
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()
        return user

async def get_user_by_id(user_id: int) -> User:
    async with LocalSession() as session:
        stmt = (
            select(User)
            .where(User.id == user_id)
        )
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()
        return user

async def get_user_by_login(login: str) -> User:
    async with LocalSession() as session:
        stmt = (
            select(User)
            .where(User.nickname == login)
        )
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()
        return user
