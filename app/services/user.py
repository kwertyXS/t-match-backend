from fastapi import HTTPException

from app.api.v1.profile import get_user_profile
from app.repository.auth import is_tg_exists, is_email_exists
from app.repository.user import update_user, get_user_by_profile
from app.schemas.user import UserSchema


async def edit_user(data: UserSchema):
    if data.telegram:
        if await is_tg_exists(data.telegram):
            raise HTTPException(status_code=400, detail="Telegram already exists")

    if data.email:
        if await is_email_exists(data.email):
            raise HTTPException(status_code=400, detail="Email already exists")
    user = await update_user(data)
    return {"nickname": user.nickname, "telegram": user.telegram, "email": user.email}

async def get_owner_profile(profile_id: int):
    if await get_user_profile(profile_id) is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return await get_user_by_profile(profile_id)