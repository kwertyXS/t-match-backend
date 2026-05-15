from fastapi import APIRouter
from app.schemas.auth import Login
from app.services.auth import login

router = APIRouter()

@router.get("/login", tags=["login"])
async def login(data: Login):
    return await login(data)



@router.get("/health")
async def health():
    return {"status": "ok"}