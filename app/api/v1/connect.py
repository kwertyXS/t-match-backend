from fastapi import APIRouter

from app.schemas.friend import FriendshipSchema

router = APIRouter()

@router.post("/connect")
async def connect_meet(data: FriendshipSchema):
    pass