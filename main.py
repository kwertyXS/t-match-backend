from fastapi import FastAPI

from app.api.v1.auth import router as auth_router
from app.api.v1.meet import router as meet_router
from app.api.v1.profile import router as profile_router
from app.api.v1.user import router as user_router
from app.api.v1.friend import router as friendship_router

app = FastAPI()

app.include_router(auth_router, prefix="/api/v1", tags=["authentication"])
app.include_router(user_router, prefix="/api/v1", tags=["user"])
app.include_router(meet_router, prefix="/api/v1", tags=["meet"])
app.include_router(profile_router, prefix="/api/v1", tags=["profile"])
app.include_router(friendship_router, prefix="/api/v1", tags=["friendship"])


