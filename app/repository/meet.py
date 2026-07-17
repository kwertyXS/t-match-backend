from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Meeting, MeetingMember, MemberRole
from app.schemas.meet import MeetingSchema, JoinToMeetingSchema
from app.validators.time import ensure_msk


async def add_meet(session: AsyncSession, data: MeetingSchema) -> Meeting:
    time_msk = await ensure_msk(data.ends_at)
    stmt = Meeting(
        title=data.title,
        description=data.description,
        ends_at=time_msk,
    )
    session.add(stmt)
    await session.commit()
    await session.refresh(stmt)
    return stmt


async def add_member(
    session: AsyncSession, meet_data: JoinToMeetingSchema, role: MemberRole
) -> MeetingMember:
    stmt = MeetingMember(
        meeting_id=meet_data.meeting_id, profile_id=meet_data.profile_id, role=role
    )
    session.add(stmt)
    await session.commit()
    await session.refresh(stmt)
    return stmt


async def get_all_meeting_members(
    session: AsyncSession, meet_id: int
) -> List[MeetingMember]:
    stmt = select(MeetingMember.profile_id, MeetingMember.role).where(
        MeetingMember.meeting_id == meet_id
    )
    result = await session.execute(stmt)
    profiles = result.all()
    return profiles


async def get_meet_by_id(session: AsyncSession, meet_id: int) -> Meeting:
    stmt = select(Meeting).where(Meeting.id == meet_id)
    result = await session.execute(stmt)
    meet = result.scalar_one_or_none()
    return meet
