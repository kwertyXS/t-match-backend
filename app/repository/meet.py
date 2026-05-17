from typing import List

from sqlalchemy import select

from app.db.models import Meeting, MeetingMember, MemberRole
from app.db.session import LocalSession
from app.schemas.meet import MeetingSchema, JoinToMeetingSchema
from app.validators.time import ensure_msk


async def add_meet(data: MeetingSchema) -> Meeting:
     async with LocalSession() as session:
        time_msk = await ensure_msk(data.ends_at)
        stmt = (
            Meeting(title = data.title,
                    description = data.description,
                    ends_at = time_msk,
                    created_by=data.created_by
            )
        )
        session.add(stmt)
        await session.commit()
        await session.refresh(stmt)
        return stmt

async def add_member(meet_data: JoinToMeetingSchema, role: MemberRole) -> MeetingMember:
     async with LocalSession() as session:
        stmt = (
            MeetingMember(meeting_id = meet_data.meeting_id,
                          profile_id = meet_data.profile_id,
                          role = role
            )
        )
        session.add(stmt)
        await session.commit()
        await session.refresh(stmt)
        return stmt


async def get_all_meeting_members(meet_id: int) -> List[MeetingMember.profile_id]:
    async with LocalSession() as session:
        stmt = (
            select(MeetingMember.profile_id)
            .where(MeetingMember.meeting_id == meet_id)
        )
        result = await session.execute(stmt)
        profiles = result.scalars().all()
        return profiles

async def get_meet_by_id(meet_id: int) -> Meeting:
    async with LocalSession() as session:
        stmt = (
            select(Meeting)
            .where(Meeting.id == meet_id)
        )
        result = await session.execute(stmt)
        meet = result.scalar_one_or_none()
        return meet
