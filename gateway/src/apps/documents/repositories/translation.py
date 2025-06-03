from fastapi import Depends
from typing import Annotated, Any, Self, Protocol
from shared.repositories.rmqrepository import RMQRPCClient
from gateway.src.apps.documents.enums import TranslateActions
from shared.settings import settings


class TranslationRepository(Protocol):
    async def translate(self: Self, textareas: Any) -> Any: ...


class RMQTranslationRepository(TranslationRepository, RMQRPCClient):
    exchange_name = "translation"

    async def translate(self: Self, textareas: Any) -> Any:
        return await self.do(TranslateActions.TRANSLATE, textareas)


async def translation_repository_factory():
    repo = RMQTranslationRepository(settings)
    await repo.initialize()
    return repo


TranslationRepositoryDep = Annotated[
    TranslationRepository,
    Depends(translation_repository_factory),
]
