import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, patch

from main import app
from app.validators.password import get_current_user


class FakeMeeting:
    id = 1
    title = "Планёрка"
    description = "Обсуждение задач"


VALID_PAYLOAD = {
    "title": "Планёрка",
    "description": "Обсуждение задач",
    "ends_at": "2025-12-31T15:00:00",
    "created_by": 42,
}


@pytest.fixture(autouse=True)
def override_auth():
    app.dependency_overrides[get_current_user] = lambda: {
        "id": 42,
        "username": "tester",
    }
    yield
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_new_meet_success():
    with patch(
        "app.services.meet.add_meet", new_callable=AsyncMock
    ) as mock_add:  # ← реальный путь
        mock_add.return_value = FakeMeeting()

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.post(
                "api/v1/meeting", json=VALID_PAYLOAD
            )  # ← реальный URL

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "title": "Планёрка",
        "description": "Обсуждение задач",
    }
    mock_add.assert_awaited_once()


@pytest.mark.asyncio
async def test_new_meet_failure():
    with patch("app.services.meet.add_meet", new_callable=AsyncMock) as mock_add:
        mock_add.return_value = None

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.post("api/v1/meeting", json=VALID_PAYLOAD)

    assert response.status_code == 200
    assert response.json() == {"ok": False}


@pytest.mark.asyncio
async def test_new_meet_invalid_payload():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post(
            "api/v1/meeting", json={"title": "только заголовок"}
        )

    assert response.status_code == 422
