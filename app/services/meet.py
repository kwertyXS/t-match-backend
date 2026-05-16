from fastapi import Depends

from app.repository.auth import get_user_by_login
from app.repository.meet import add_meet
from app.schemas.meet import MeetingSchema
from app.validators.password import get_current_user


async def new_meet(data: MeetingSchema, current_user: dict = Depends(get_current_user)):
    meet = await add_meet(data)
    if meet is not None:
        return {"id": meet.id, "title": meet.title, "description": meet.description}
    else:
        return {"ok": False}