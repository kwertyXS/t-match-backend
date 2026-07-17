from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User
from app.validators.password import hash_password


async def is_user_exists(session: AsyncSession, login: str) -> bool:
    stmt = select(User.id).where(User.nickname == login).limit(1)
    result = await session.execute(stmt)
    user_id = result.scalar()
    return user_id is not None


async def add_user(session: AsyncSession, data, refresh_token) -> User:
    hashed_password = await hash_password(data.password)
    user = User(
        nickname=data.login,
        password_hash=hashed_password,
        email=data.email,
        telegram=data.telegram,
        refresh_token=refresh_token,
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def get_refresh_token(session: AsyncSession, refresh_token: str) -> User:
    stmt = select(User).where(User.refresh_token == refresh_token)
    result = await session.execute(stmt)
    user = result.scalar()
    return user


async def update_refresh_token(session: AsyncSession, login, refresh_token) -> User:
    stmt = select(User).where(User.nickname == login)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    user.refresh_token = refresh_token
    await session.commit()
    return user


async def is_tg_exists(session: AsyncSession, tg: str) -> bool:
    stmt = select(User).where(User.telegram == tg)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    return user is not None


async def is_email_exists(session: AsyncSession, email: str) -> bool:
    stmt = select(User).where(User.email == email)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    return user is not None
