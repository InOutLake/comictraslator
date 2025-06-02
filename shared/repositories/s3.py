from contextlib import asynccontextmanager
from typing import Annotated, Protocol
from aioboto3 import Session
from botocore.config import Config
from fastapi import Depends
from shared.settings import Settings, settings
from typing import Self
from datetime import datetime


class S3Repository(Protocol):
    async def upload(self: Self, file: bytes) -> str: ...
    async def get_download_url(self: Self, filename: str) -> str: ...


class S3AioBotoRepository(S3Repository):
    def __init__(self: Self, settings: Settings):
        self.session = Session()
        self.settings = settings
        self.bucketname = settings.S3_BUCKET_NAME

    @asynccontextmanager
    async def client(self: Self):
        yield self.session.client(
            "s3",
            endpoint_url=self.settings.S3_ENDPOINT_URL,
            aws_access_key_id=self.settings.S3_ACCESS_KEY,
            aws_secret_access_key=self.settings.S3_SECRET_KEY,
            region_name="us-east-1",
            config=Config(signature_version="s3v4"),
        )

    async def upload(self: Self, file: bytes) -> str:
        async with self.client() as client:
            now = datetime.now()
            filename = str(now.timestamp) + str(now.microsecond)
            response = await client.upload_fileobj(
                Key=filename,
                Bucket_name=self.bucketname,
            )
            return response

    async def get_download_url(self: Self, filename: str) -> str:
        async with self.client() as client:
            url = await client.generate_presigned_url(
                "get_object",
                Params={"Bucket": self.bucketname, "Key": filename},
                ExpiresIn=3600,
            )
            return url


def s3_repository_factory(settings=settings) -> S3Repository:
    return S3AioBotoRepository(settings)


S3RepositoryDep = Annotated[S3Repository, Depends(s3_repository_factory)]
