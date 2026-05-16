from fastapi import APIRouter, Depends

from app.schemas.user import UserSchema
from app.services.user import edit_user
from app.validators.password import get_current_user

router = APIRouter()

@router.patch("/user")
async def update_user(data: UserSchema, current_user: dict = Depends(get_current_user)):
    """изменение юзера"""
    return await edit_user(data)
