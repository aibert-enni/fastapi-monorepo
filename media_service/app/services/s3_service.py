import logging
from contextlib import asynccontextmanager
from typing import Any, AsyncIterator, Awaitable, BinaryIO, Callable, TypeVar

from aiobotocore.session import AioBaseClient, get_session
from botocore.exceptions import (
    ClientError,
    EndpointConnectionError,
    NoCredentialsError,
    NoRegionError,
    ParamValidationError,
)

from app.core.settings import settings
from app.exceptions.custom_exceptions import ServiceUnavailableError

logger = logging.getLogger(__name__)

T = TypeVar("T")


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

    async def _call(
        self,
        function: Callable[..., Awaitable[T]],
        handled_exceptions: tuple[type[BaseException], ...] = (),
        *args: Any,
        **kwargs: Any,
    ) -> T:
        """
        Call S3 function with error handling
        """
        try:
            return await function(*args, **kwargs)
        except handled_exceptions as e:
            raise e
        except ParamValidationError as e:
            logger.error(f"S3 params error: {e}")
            raise ServiceUnavailableError
        except ClientError as e:
            logger.error(f"S3 client error: {e}")
            raise ServiceUnavailableError
        except Exception as e:
            logger.error(f"S3 unknown error: {e}")
            raise ServiceUnavailableError

    @asynccontextmanager
    async def get_client(self) -> AsyncIterator[AioBaseClient]:
        try:
            async with self.session.create_client("s3", **self.config) as client:
                yield client
        except (NoCredentialsError, NoRegionError) as e:
            logger.error(f"S3 config error: {e}")
            raise ServiceUnavailableError
        except EndpointConnectionError as e:
            logger.error(f"S3 endpoint unreachable: {e}")
            raise ServiceUnavailableError
        except Exception as e:
            logger.error(f"S3 unknown error: {e}")
            raise ServiceUnavailableError

    def get_public_url(self, key: str) -> str:
        url = f"{self.config['endpoint_url']}/{self.bucket_name}/{key}"
        return url

    async def get_private_url(self, key: str, expire: int) -> str:
        async with self.get_client() as client:
            url = await client.generate_presigned_url(
                "get_object",
                Params={"Bucket": self.bucket_name, "Key": key},
                ExpiresIn=expire,
            )  # type: ignore
        return url

    async def public_upload(self, body: BinaryIO, key: str, content_type: str) -> None:
        """
        Upload file to S3 and get public url
        """
        async with self.get_client() as client:
            await self._call(
                client.put_object,
                Body=body,
                Bucket=self.bucket_name,
                Key=key,
                ContentType=content_type,
                ACL="public-read",
            )

    async def private_upload(
        self, body: BinaryIO, key: str, content_type: str, expire: int = 3600
    ) -> None:
        """
        Upload file to S3 and get private url
        """
        async with self.get_client() as client:
            await self._call(
                client.put_object,
                Body=body,
                Bucket=self.bucket_name,
                Key=key,
                ContentType=content_type,
            )

    async def delete(self, key: str) -> None:
        async with self.get_client() as client:
            return await self._call(
                client.delete_object, Bucket=self.bucket_name, Key=key
            )


s3_client = S3Client(
    access_key=settings.s3.access_key,
    secret_key=settings.s3.secret_key,
    endpoint_url=settings.s3.endpoint_url,
    bucket_name=settings.s3.bucket_name,
)
