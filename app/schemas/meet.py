from datetime import datetime

from pydantic import BaseModel


class MeetingSchema(BaseModel):
    title: str
    description: str
    ends_at: datetime

class JoinToMeetingSchema(BaseModel):
    profile_id: int
    meeting_id: int


class MeetingMemberResponseSchema(BaseModel):
    profile_id: int
    role: str


