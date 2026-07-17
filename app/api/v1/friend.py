from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.friend import FriendshipSchema, FriendshipAnswerSchema
from app.services.friend import (
    add_friendship,
    accept_friend,
    deny_friendship,
    get_user_friends,
)
from app.validators.password import get_current_user

router = APIRouter()


@router.post("/friendship")
async def friends(
    data: FriendshipSchema,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return await add_friendship(db, data, current_user)


@router.post("/accept")
async def add_friend(
    data: FriendshipSchema,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return await accept_friend(db, data, current_user)


@router.delete("/deny")
async def deny_friend(
    data: FriendshipSchema,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return await deny_friendship(db, data, current_user)


@router.get("/friends")
async def get_friends(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
) -> List[FriendshipAnswerSchema]:
    return await get_user_friends(db, current_user)
