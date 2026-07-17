from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Friend


async def add_users_friendship(session: AsyncSession, user1: int, user2: int) -> Friend:
    friendship = Friend(user_id=user1, friend_id=user2)
    session.add(friendship)
    await session.commit()
    await session.refresh(friendship)
    return friendship


async def accept_friendship(session: AsyncSession, user1: int, user2: int) -> Friend:
    stmt = select(Friend).where(Friend.user_id == user1 and Friend.friend_id == user2)
    result = await session.execute(stmt)
    friendship = result.scalar_one_or_none()
    if friendship:
        friendship.accept = True
        await session.commit()
        await session.refresh(friendship)
    return friendship


async def deny_friend(session: AsyncSession, user1: int, user2: int):
    stmt = select(Friend).where(Friend.user_id == user1 and Friend.friend_id == user2)
    result = await session.execute(stmt)
    friendship = result.scalar_one_or_none()
    if friendship:
        await session.delete(friendship)
        await session.commit()


async def is_friendship_exists(session: AsyncSession, user1: int, user2: int):
    stmt = select(Friend).where(Friend.user_id == user1 and Friend.friend_id == user2)
    result = await session.execute(stmt)
    friendship = result.scalar_one_or_none()
    if friendship:
        return True
    return False


async def get_friends(session: AsyncSession, user_id: int):
    stmt = select(Friend).where(
        Friend.accept & ((Friend.user_id == user_id) | (Friend.friend_id == user_id))
    )
    result = await session.execute(stmt)
    friends = result.scalars().all()
    return friends
