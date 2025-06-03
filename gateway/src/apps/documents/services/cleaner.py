from apps.documents.schemas.services.cleaner import CleanRequest, CleanResponse
from fastapi import Depends
from typing import Annotated, Any, Protocol, Self
from gateway.src.apps.documents.repositories.cleaner import (
    CleanerRepository,
    CleanerRepositoryDep,
)


class CleanerService(Protocol):
    async def clean(self: Self, data: CleanRequest) -> CleanResponse: ...


class CleanerServiceImpl(CleanerService):
    def __init__(self: Self, cleaner: CleanerRepository):
        self.cleaner = cleaner

    async def clean(self: Self, data: CleanRequest) -> CleanResponse:
        cleaned_url = await self.cleaner.clean(data)
        return CleanResponse.model_validate_json(cleaned_url)


def cleaner_service_factory(cleaner: CleanerRepositoryDep):
    return CleanerServiceImpl(cleaner=cleaner)


CleanerServiceDep = Annotated[CleanerService, Depends(cleaner_service_factory)]
