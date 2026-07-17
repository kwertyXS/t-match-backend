import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, patch

from main import app
from app.validators.password import get_current_user

PAYLOAD = {"user_login": "friend_user"}

FAKE_USER_1 = type("User", (), {"id": 1, "login": "current_user"})()
FAKE_USER_2 = type("User", (), {"id": 2, "login": "friend_user"})()
FAKE_FRIENDSHIP = {"user1": 1, "user2": 2, "accepted": False}


@pytest.fixture(autouse=True)
def override_auth():
    app.dependency_overrides[get_current_user] = lambda: {
        "id": 1,
        "login": "current_user",
    }
    yield
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_add_friendship_success():
    with (
        patch(
            "app.services.friend.get_user_by_login", new_callable=AsyncMock
        ) as mock_get,
        patch(
            "app.services.friend.is_friendship_exists", new_callable=AsyncMock
        ) as mock_exists,
        patch(
            "app.services.friend.add_users_friendship", new_callable=AsyncMock
        ) as mock_add,
    ):
        mock_get.side_effect = [FAKE_USER_1, FAKE_USER_2]
        mock_exists.return_value = False
        mock_add.return_value = FAKE_FRIENDSHIP

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.post("/api/v1/friendship", json=PAYLOAD)

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_add_friendship_already_exists():
    with (
        patch(
            "app.services.friend.get_user_by_login", new_callable=AsyncMock
        ) as mock_get,
        patch(
            "app.services.friend.is_friendship_exists", new_callable=AsyncMock
        ) as mock_exists,
        patch("app.services.friend.add_users_friendship", new_callable=AsyncMock),
    ):
        mock_get.side_effect = [FAKE_USER_1, FAKE_USER_2]
        mock_exists.return_value = True

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.post("/api/v1/friendship", json=PAYLOAD)

    assert response.status_code == 400
    assert response.json()["detail"] == "Friendship already exists"


@pytest.mark.asyncio
async def test_add_friendship_same_user():
    SAME_USER = type("User", (), {"id": 1, "login": "current_user"})()

    with patch(
        "app.services.friend.get_user_by_login", new_callable=AsyncMock
    ) as mock_get:
        mock_get.side_effect = [SAME_USER, SAME_USER]

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.post(
                "/api/v1/friendship", json={"user_login": "current_user"}
            )

    assert response.status_code == 403
    assert response.json()["detail"] == "User can't be same"


@pytest.mark.asyncio
async def test_add_friendship_user_not_found():
    with patch(
        "app.services.friend.get_user_by_login", new_callable=AsyncMock
    ) as mock_get:
        mock_get.side_effect = [None, None]

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.post("/api/v1/friendship", json=PAYLOAD)

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_accept_friend_success():
    with (
        patch(
            "app.services.friend.get_user_by_login", new_callable=AsyncMock
        ) as mock_get,
        patch(
            "app.services.friend.accept_friendship", new_callable=AsyncMock
        ) as mock_accept,
    ):
        mock_get.side_effect = [FAKE_USER_1, FAKE_USER_2]
        mock_accept.return_value = FAKE_FRIENDSHIP

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.post("/api/v1/accept", json=PAYLOAD)

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_deny_friendship_success():
    with (
        patch(
            "app.services.friend.get_user_by_login", new_callable=AsyncMock
        ) as mock_get,
        patch("app.services.friend.deny_friend", new_callable=AsyncMock) as mock_deny,
    ):
        mock_get.side_effect = [FAKE_USER_1, FAKE_USER_2]
        mock_deny.return_value = None

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.request("DELETE", "/api/v1/deny", json=PAYLOAD)

    assert response.status_code == 200
    assert response.json() == {"ok": True}
