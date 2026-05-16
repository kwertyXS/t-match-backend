from sqlalchemy import select

from app.db.models import  Friend
from app.db.session import LocalSession

async def add_users_friendship(user1: int, user2: int) -> Friend:
    async with LocalSession() as session:
        friendship = (
            Friend(user_id=user1, friend_id=user2)
        )
        session.add(friendship)
        await session.commit()
        await session.refresh(friendship)
        return friendship


async def accept_friendship(user1: int, user2: int) -> Friend:
    async with LocalSession() as session:
        stmt = (
            select(Friend)
            .where(Friend.user_id == user1 and Friend.friend_id == user2)
        )
        result = await session.execute(stmt)
        friendship = result.scalar_one_or_none()
        if friendship:
            friendship.accept = True
            await session.commit()
            await session.refresh(friendship)
        return friendship

async def deny_friend(user1: int, user2: int):
    async with LocalSession() as session:
        stmt = (
            select(Friend)
            .where(Friend.user_id == user1 and Friend.friend_id == user2)
        )
        result = await session.execute(stmt)
        friendship = result.scalar_one_or_none()
        if friendship:
            await session.delete(friendship)
            await session.commit()
