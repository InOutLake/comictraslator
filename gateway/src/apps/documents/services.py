from typing import Any, Protocol, Annotated, Self

from fastapi import Depends

from src.tools.settings import Settings
from src.apps.documents.schemas import Document, DBDocumentSchema
from src.apps.documents.repository import DocumentsRepositoryProtocol


class DocumentsServiceProtocol(Protocol):
    async def read_docuemnt(self: Self, document_data: DBDocumentSchema) -> Document: ...


class DocumentServiceImpl:
    def __init__(self, repository: DocumentsRepositoryProtocol) -> None:
        self.repository: Any = repository

    async def read_document(self: Self, document: Document):
        return await self.repository.read_document(document)


class DocumentFactoryProtocol(Protocol):
    async def make(self: Self, provider: str) -> DocumentsServiceProtocol: ...


class DocumentFactoryImpl:
    def __init__(self: Self, settings: Settings) -> None:
        self.settings = settings

    async def make(self: Self, provider: str) -> DocumentsServiceProtocol: ...


async def get_document_factory(settings: Settings) -> DocumentFactoryProtocol:
    return DocumentFactoryImpl(settings)


DocumentFactory = Annotated[DocumentFactoryProtocol, Depends(get_document_factory)]
