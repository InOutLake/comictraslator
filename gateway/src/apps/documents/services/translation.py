from fastapi import Depends
from typing import Annotated, Any, Self, Protocol

from gateway.src.apps.documents.repositories.translation import (
    TranslationRepository,
    TranslationRepositoryDep,
)


class TranslationService(Protocol):
    async def translate(self: Self, textareas: Any) -> Any: ...


class TranslationServiceImpl(TranslationService):
    def __init__(self: Self, repo: TranslationRepository):
        self.repo = repo

    async def translate(self: Self, textareas: Any) -> Any:
        return self.repo.translate(textareas)


def translation_service_factory(repo: TranslationRepositoryDep):
    return TranslationServiceImpl(repo)


TranslationServiceDep = Annotated[
    TranslationService, Depends(translation_service_factory)
]
