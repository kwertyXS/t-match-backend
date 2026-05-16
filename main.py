from fastapi import FastAPI

from app.api.v1.auth import router as auth_router
from app.api.v1.meet import router as meet_router
from app.api.v1.prof import router as prof_router

app = FastAPI()

app.include_router(auth_router, prefix="/api/v1", tags=["authentication"])
app.include_router(meet_router, prefix="/api/v1", tags=["meet"])
app.include_router(prof_router, prefix="/api/v1", tags=["profile"])



