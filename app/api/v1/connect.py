from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.friend import FriendshipSchema

router = APIRouter()


@router.post("/connect")
async def connect_meet(data: FriendshipSchema, db: AsyncSession = Depends(get_db)):
    pass
