import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, patch

from main import app
from app.validators.password import get_current_user

FAKE_USER = type("User", (), {"id": 1, "login": "testuser"})()
FAKE_PROFILE = type(
    "Profile",
    (),
    {
        "id": 1,
        "user_id": 1,
        "title": "My Profile",
        "description": "Test desc",
        "tags": ["python", "fastapi"],
    },
)()

CREATE_PAYLOAD = {
    "title": "My Profile",
    "description": "Test desc",
    "tags": ["python", "fastapi"],
}
UPDATE_PAYLOAD = {
    "id": 1,
    "title": "Updated",
    "description": "New desc",
    "tags": ["updated"],
}


@pytest.fixture(autouse=True)
def override_auth():
    app.dependency_overrides[get_current_user] = lambda: {"id": 1, "login": "testuser"}
    yield
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_get_profile_success():
    with patch(
        "app.services.profile.get_user_profile", new_callable=AsyncMock
    ) as mock_get:
        mock_get.return_value = FAKE_PROFILE

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get("/api/v1/profile/1")

    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["title"] == "My Profile"


@pytest.mark.asyncio
async def test_get_user_profiles_success():
    with (
        patch(
            "app.services.profile.get_user_by_login", new_callable=AsyncMock
        ) as mock_user,
        patch(
            "app.services.profile.get_profiles", new_callable=AsyncMock
        ) as mock_profiles,
    ):
        mock_user.return_value = FAKE_USER
        mock_profiles.return_value = [FAKE_PROFILE]

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get("/api/v1/profiles")

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_new_profile_success():
    with (
        patch(
            "app.services.profile.get_user_by_login", new_callable=AsyncMock
        ) as mock_user,
        patch("app.services.profile.add_profile", new_callable=AsyncMock) as mock_add,
    ):
        mock_user.return_value = FAKE_USER
        mock_add.return_value = FAKE_PROFILE

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.post("/api/v1/profile", json=CREATE_PAYLOAD)

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "title": "My Profile",
        "description": "Test desc",
        "tags": ["python", "fastapi"],
    }


@pytest.mark.asyncio
async def test_new_profile_failure():
    with (
        patch(
            "app.services.profile.get_user_by_login", new_callable=AsyncMock
        ) as mock_user,
        patch("app.services.profile.add_profile", new_callable=AsyncMock) as mock_add,
    ):
        mock_user.return_value = FAKE_USER
        mock_add.return_value = None

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.post("/api/v1/profile", json=CREATE_PAYLOAD)

    assert response.status_code == 200
    assert response.json() == {"ok": False}


@pytest.mark.asyncio
async def test_new_profile_title_too_short():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post(
            "/api/v1/profile", json={"title": "ab", "description": "desc", "tags": []}
        )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_new_profile_title_too_long():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post(
            "/api/v1/profile",
            json={"title": "a" * 31, "description": "desc", "tags": []},
        )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_edit_profile_success():
    with patch(
        "app.services.profile.update_profile", new_callable=AsyncMock
    ) as mock_update:
        mock_update.return_value = type(
            "Profile",
            (),
            {"title": "Updated", "description": "New desc", "tags": ["updated"]},
        )()

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.patch("/api/v1/profile", json=UPDATE_PAYLOAD)

    assert response.status_code == 200
    assert response.json() == {
        "title": "Updated",
        "description": "New desc",
        "tags": ["updated"],
    }
