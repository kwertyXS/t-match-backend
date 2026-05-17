from datetime import datetime

from pydantic import BaseModel


class MeetingSchema(BaseModel):
    title: str
    description: str
    ends_at: datetime
    created_by: int

class JoinToMeetingSchema(BaseModel):
    profile_id: int
    meeting_id: int

