from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import MemberRole
from app.repository.meet import (
    add_meet,
    add_member,
    get_all_meeting_members,
    get_meet_by_id,
)
from app.repository.profile import get_profile_by_id
from app.schemas.meet import (
    MeetingSchema,
    JoinToMeetingSchema,
    MeetingMemberResponseSchema,
)
from app.validators.password import get_current_user


async def new_meet(
    session: AsyncSession,
    data: MeetingSchema,
    current_user: dict = Depends(get_current_user),
):
    meet = await add_meet(session, data)
    if meet is not None:
        return {"id": meet.id, "title": meet.title, "description": meet.description}
    else:
        return {"ok": False}


async def new_meet_member(session: AsyncSession, meet_data: JoinToMeetingSchema):
    role = MemberRole.MEMBER
    members = await get_all_meeting_members(session, meet_data.meeting_id)
    if len(members) == 0:
        role = MemberRole.ADMIN
    if meet_data.profile_id in members:
        raise HTTPException(status_code=400, detail="User already on meet")
    if await get_meet_by_id(session, meet_data.meeting_id) is None:
        raise HTTPException(status_code=403, detail="Meet not found")
    if await get_profile_by_id(session, meet_data.profile_id) is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    member = await add_member(session, meet_data, role)
    if member is not None:
        return {
            "id": member.id,
            "meeting_id": member.meeting_id,
            "profile_id": member.profile_id,
        }
    else:
        return {"ok": False}


async def get_all_meeting_profiles(session: AsyncSession, meet_id: int):
    members = await get_all_meeting_members(session, meet_id)
    return [
        MeetingMemberResponseSchema(profile_id=row.profile_id, role=row.role)
        for row in members
    ]
