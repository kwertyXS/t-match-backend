import sys
import os
import asyncio

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

os.environ["PG_URL"] = "sqlite+aiosqlite:///:memory:"
os.environ["SECRET_KEY"] = "test-secret-key"
os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = "30"
os.environ["ALGORITHM"] = "HS256"
os.environ["REFRESH_TOKEN_EXPIRE_DAYS"] = "7"

import pytest

from app.db.models import Base
from app.db.session import get_engine
from main import app
from app.validators.password import get_current_user


def pytest_sessionstart():
    engine = get_engine()

    async def init():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    asyncio.run(init())


def pytest_sessionfinish():
    engine = get_engine()

    async def cleanup():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    asyncio.run(cleanup())


@pytest.fixture(autouse=True)
def override_auth():
    app.dependency_overrides[get_current_user] = lambda: {"id": 1, "login": "testuser"}
    yield
    app.dependency_overrides.clear()
