from typing import List

from fastapi import APIRouter, Depends

from app.schemas.friend import FriendshipSchema, FriendshipAnswerSchema
from app.services.friend import add_friendship, accept_friend, deny_friendship, get_user_friends
from app.validators.password import get_current_user

router = APIRouter()

@router.post("/friendship")
async def friends(data: FriendshipSchema,
                  current_user: dict = Depends(get_current_user)):
    """Создание предложения дружбы"""
    return await add_friendship(data, current_user)

@router.post("/accept")
async def add_friend(data: FriendshipSchema,
                     current_user: dict = Depends(get_current_user)):
    """Принятие предложения дружбы"""
    return await accept_friend(data, current_user)

@router.delete("/deny")
async def deny_friend(data: FriendshipSchema,
                      current_user: dict = Depends(get_current_user)):
    """Отклонение предложения дружбы"""
    return await deny_friendship(data, current_user)

@router.get("/friends")
async def get_friends(current_user: dict = Depends(get_current_user)) -> List[FriendshipAnswerSchema]:
    return await get_user_friends(current_user)
