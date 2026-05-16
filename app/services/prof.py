from fastapi import Depends

from app.repository.auth import get_user_by_login
from app.repository.prof import add_profile
from app.schemas.profile import ProfileSchema
from app.validators.password import get_current_user


async def new_profile(data: ProfileSchema, current_user: dict = Depends(get_current_user)):
    user = await get_user_by_login(current_user['login'])
    prof = await add_profile(data, user.id)
    if prof is not None:
        return {"id": prof.id, "title": prof.title, "description": prof.description, "tags": prof.tags}
    else:
        return {"ok": False}