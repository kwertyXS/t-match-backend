from fastapi import APIRouter

from app.schemas.friend import FriendshipSchema
from app.services.friend import add_friendship, accept_friend, deny_friendship

router = APIRouter()

@router.post("/friendship")
async def friends(data: FriendshipSchema):
    """Создание предложения дружбы"""
    return await add_friendship(data)

@router.post("/accept")
async def add_friend(data: FriendshipSchema):
    """Принятие предложения дружбы"""
    return await accept_friend(data)

@router.delete("/deny")
async def deny_friend(data: FriendshipSchema):
    """Отклонение предложения дружбы"""
    return await deny_friendship(data)
