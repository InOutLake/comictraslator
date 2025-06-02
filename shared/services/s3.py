from shared.repositories.s3 import S3RepositoryDep, S3Repository
from typing import Protocol, Self, Annotated
from fastapi import Depends


class S3Service(Protocol):
    async def upload(self: Self, file: bytes) -> str: ...
    async def get_url(self: Self, filename: str) -> str: ...


class S3ServiceImpl(S3Service):
    def __init__(self: Self, repo: S3Repository):
        self.repo = repo

    async def upload(self: Self, file: bytes) -> str:
        return await self.repo.upload(file)

    async def get_url(self: Self, filename: str) -> str:
        return await self.repo.get_download_url(filename)


def s3_service_factory(s3_repo: S3RepositoryDep):
    return S3ServiceImpl(s3_repo)


S3ServiceDep = Annotated[S3Service, Depends(s3_service_factory)]
