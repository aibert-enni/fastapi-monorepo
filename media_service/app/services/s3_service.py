from contextlib import asynccontextmanager
from io import IOBase
from typing import AsyncIterator

from aiobotocore.session import AioBaseClient, get_session

from app.core.settings import settings


class S3Client:
    def __init__(
        self, access_key: str, secret_key: str, endpoint_url: str, bucket_name: str
    ):
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url,
        }
        self.bucket_name = bucket_name
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self) -> AsyncIterator[AioBaseClient]:
        async with self.session.create_client("s3", **self.config) as client:
            yield client

    async def upload(self, body: IOBase, key: str, content_type: str) -> str:
        async with self.get_client() as client:
            resp = await client.put_object(
                Body=body,
                Bucket=self.bucket_name,
                Key=key,
                ACL="public-read",
                ContentType=content_type,
            )  # type: ignore
            print(resp)
            url = f"{self.config.get('endpoint_url')}/{self.bucket_name}/{key}"
            print(url)
            return url


s3_client = S3Client(
    access_key=settings.s3.access_key,
    secret_key=settings.s3.secret_key,
    endpoint_url=settings.s3.endpoint_url,
    bucket_name=settings.s3.bucket_name,
)
