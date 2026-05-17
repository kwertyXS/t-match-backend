from fastapi import Depends, HTTPException

from app.db.models import MemberRole
from app.repository.meet import add_meet, add_member, get_all_meeting_members, get_meet_by_id
from app.repository.profile import get_profile_by_id
from app.schemas.meet import MeetingSchema, JoinToMeetingSchema
from app.validators.password import get_current_user


async def new_meet(data: MeetingSchema, current_user: dict = Depends(get_current_user)):
    meet = await add_meet(data)
    if meet is not None:
        return {"id": meet.id, "title": meet.title, "description": meet.description}
    else:
        return {"ok": False}

async def new_meet_member(meet_data: JoinToMeetingSchema):
    role = MemberRole.MEMBER
    members = await get_all_meeting_members(meet_data.meeting_id)
    if len(members) == 0:
        role = MemberRole.ADMIN
    if meet_data.profile_id in members:
        raise HTTPException(status_code=400, detail="User already on meet")
    if await get_meet_by_id(meet_data.meeting_id) is None:
        raise HTTPException(status_code=403, detail="Meet not found")
    if await get_profile_by_id(meet_data.profile_id) is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    member = await add_member(meet_data, role)
    if member is not None:
        return {"id": member.id, "meeting_id": member.meeting_id, "profile_id": member.profile_id}
    else:
        return {"ok": False}

async def get_all_meeting_profiles(meet_id: int):
    members = await get_all_meeting_members(meet_id)
    return members
