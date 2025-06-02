from typing import Any, Protocol, Annotated, Self

from fastapi import Depends

from src.apps.documents.repositories.ocr import OCRRepository, OCRRepositoryDep
from src.common.settings import settings
from src.apps.documents.schemas import Document, DBDocumentSchema


class DocumentsServiceProtocol(Protocol):
    async def 

class DocumentServiceImpl(DocumentsServiceProtocolk):
    def __init__(self, ocr: OCRRepositoryDep) -> None:
        self.ocr: OCRRepository = ocr

    def translate(self: Self):


# class DocumentFactoryProtocol(Protocol):
#     async def make(self: Self, provider: str) -> DocumentsServiceProtocol: ...


# class DocumentFactoryImpl:
#     def __init__(self: Self, settings: Settings) -> None:
#         self.settings = settings

#     async def make(self: Self, provider: str) -> DocumentsServiceProtocol: ...


# async def get_document_factory(settings: Settings) -> DocumentFactoryProtocol:
#     return DocumentFactoryImpl(settings)


# DocumentFactory = Annotated[DocumentFactoryProtocol, Depends(get_document_factory)]
