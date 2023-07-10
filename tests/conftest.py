import asyncio
from typing import Generator

import pytest as pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from httpx import AsyncClient

from app.core.security.jwt_token_manager import get_access_token
from app.main import app
from configuration.configs import settings


@pytest_asyncio.fixture(scope="session")
async def async_client() -> Generator:
    async with AsyncClient(
            app=app,
            base_url=f"http://{settings.API_URL}"
    ) as client, LifespanManager(app):
        yield client


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def token_jtw_admin_user() -> str:
    token = get_access_token(settings.ONE_ADMIN_USER_ID)
    bearer_token = "Bearer " + token
    return bearer_token
