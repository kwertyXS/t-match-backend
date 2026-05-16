from fastapi import APIRouter, Depends
from app.services.prof import new_profile
from app.schemas.profile import ProfileSchema
from app.validators.password import get_current_user

router = APIRouter()

@router.post("/profile")
async def profile(data: ProfileSchema,
                  current_user: dict = Depends(get_current_user)):
    return await new_profile(data, current_user)