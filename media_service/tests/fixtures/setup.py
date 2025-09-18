import pytest_asyncio

from app.core.settings import settings


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup():
    settings.file.default_expire_seconds = 5
