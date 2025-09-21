import pytest_asyncio

from app.core.settings import settings
from app.services.s3_service import s3_client


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup():
    settings.file.default_expire_seconds = 5
    s3_client.bucket_name = "test"
    s3_client.config.update({"endpoint_url": "http://localhost:9002"})
