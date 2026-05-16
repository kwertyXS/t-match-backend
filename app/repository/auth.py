from sqlalchemy import select

from app.db.models import User
from app.db.session import LocalSession
from app.validators.password import hash_password



async def is_user_exists(login: str) -> bool:
    async with LocalSession() as session:
        stmt = (
            select(User.id)
            .where(User.nickname == login)
            .limit(1)
        )
        result = await session.execute(stmt)
        user_id = result.scalar()

        return user_id is not None

async def add_user(data) -> User:
    async with LocalSession() as session:
        print(data.password)
        hashed_password = await hash_password(data.password)
        user = (
            User(
                nickname=data.login,
                password_hash=hashed_password,
            )
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

async def get_user_by_login(login: str) -> User:
    async with LocalSession() as session:
        stmt = (
            select(User)
            .where(User.nickname == login)
        )
        result = await session.execute(stmt)
        user = result.scalar()
        return user