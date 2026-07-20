import time

from fastapi import APIRouter
from fastapi.security import HTTPBearer


router = APIRouter()
security = HTTPBearer()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.get("/get_time")
def get_time():
    return {"time": str(time.time()), "status": "ok"}
