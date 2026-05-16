from sqlalchemy import select

from app.db.models import User
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
