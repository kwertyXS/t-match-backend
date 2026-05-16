from app.repository.user import update_user
from app.schemas.user import UserSchema


async def edit_user(data: UserSchema):
    user = await update_user(data)
    return {"nickname": user.nickname, "telegram": user.telegram, "email": user.email}