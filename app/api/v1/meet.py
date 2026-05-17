from fastapi import APIRouter, Depends
from app.services.meet import new_meet, new_meet_member, get_all_meeting_profiles
from app.schemas.meet import MeetingSchema, JoinToMeetingSchema
from app.validators.password import get_current_user

router = APIRouter()

@router.post("/meeting")
async def meeting(data: MeetingSchema,
                  current_user: dict = Depends(get_current_user)):
    """Создание встречи"""
    return await new_meet(data, current_user)

@router.post("/meeting/join_user")
async def join_user(meet_data: JoinToMeetingSchema):
    """Добавление участника на встречу"""
    return await new_meet_member(meet_data)

@router.get("/meeting/{id}")
async def get_all_meeting_members(id: int):
    return await get_all_meeting_profiles(id)