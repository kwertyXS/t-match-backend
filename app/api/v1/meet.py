from fastapi import APIRouter, Depends
from app.services.meet import new_meet
from app.schemas.meet import MeetingSchema
from app.validators.password import get_current_user

router = APIRouter()

@router.post("/meeting")
async def meeting(data: MeetingSchema,
                  current_user: dict = Depends(get_current_user)):
    """Создание встречи"""
    return await new_meet(data, current_user)