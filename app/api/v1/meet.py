from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.services.meet import new_meet, new_meet_member, get_all_meeting_profiles
from app.schemas.meet import (
    MeetingSchema,
    JoinToMeetingSchema,
    MeetingMemberResponseSchema,
)
from app.validators.password import get_current_user

router = APIRouter()


@router.post("/meeting")
async def meeting(
    data: MeetingSchema,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return await new_meet(db, data, current_user)


@router.post("/meeting/join_user")
async def join_user(meet_data: JoinToMeetingSchema, db: AsyncSession = Depends(get_db)):
    return await new_meet_member(db, meet_data)


@router.get("/meeting/{id}")
async def get_all_meeting_members(
    id: int, db: AsyncSession = Depends(get_db)
) -> List[MeetingMemberResponseSchema]:
    return await get_all_meeting_profiles(db, id)
