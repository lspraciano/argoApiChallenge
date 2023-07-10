import pytest
from httpx import AsyncClient

from configuration.configs import settings


@pytest.mark.anyio
async def test_user_authentication(
        async_client: AsyncClient
):
    data: dict = {
        "username": settings.ONE_ADMIN_USER_EMAIL,
        "password": settings.ONE_ADMIN_PASSWORD,
    }
    response = await async_client.post(
        "users/authentication",
        data=data,
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        },
    )
    response_json = response.json()

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "user_email" in response.json()
    assert "user_id" in response.json()
    assert response_json["user_email"] == settings.ONE_ADMIN_USER_EMAIL
    assert response_json["user_id"] == settings.ONE_ADMIN_USER_ID
