from fastapi import HTTPException, Depends

from app.api.v1.profile import get_user_profile
from app.repository.auth import is_tg_exists, is_email_exists
from app.repository.user import update_user, get_user_by_profile, get_user_by_id, get_user_by_login
from app.schemas.user import UserSchema, UserResponseSchema
from app.validators.password import get_current_user


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
    user = await get_user_by_id(profile_id)
    return UserResponseSchema(user_id=user.id, nickname=user.nickname, telegram=user.telegram, email=user.email)

async def find_user(user_id: int):
    user = await get_user_by_id(user_id)
    print("USERRRRR", user)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponseSchema(user_id=user.id, nickname=user.nickname, telegram=user.telegram, email=user.email)

async def get_user_by_token(current_user: dict = Depends(get_current_user)):
    user = await get_user_by_login(current_user['login'])

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserResponseSchema(user_id=user.id, nickname=user.nickname, telegram=user.telegram, email=user.email)
