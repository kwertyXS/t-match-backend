from fastapi import APIRouter
from fastapi.security import HTTPBearer


router = APIRouter()
security = HTTPBearer()


@router.get("/health")
def health():
    return {"status": "ok"}
