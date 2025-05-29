from typing import Annotated, Protocol, Self, List

from fastapi import Depends
from src.apps.documents.services import DocumentFactory, DocumentFactoryProtocol
from src.apps.documents.schemas import Document, DBDocumentSchema


class DocumentsUseCaseProtocol(Protocol):
    async def list_documents(self: Self, doc_data: List[DBDocumentSchema]) -> list[Document]: ...

    # async def read_document(self: Self, doc_data: DBDocumentSchema) -> Document: ...

    # async def save_document(self: Self, doc_data: SaveDocumentSchema) -> Document: ...

    # async def acquire_fields(self: Self, doc_data: AcquireFieldsDocuemtnSchema) -> Document: ...

    # async def translate_document(self: Self, doc_data: TranslateDocumentSchema) -> Document: ...


class DocumentsUseCaseImpl:
    def __init__(self, document_factory: DocumentFactoryProtocol):
        self.document_factory = document_factory

    # async def read_document(self: Self, doc_data: DBDocumentSchema) -> Document:
    #     print(doc_data)
    #     return Document(owner=1, pages=None)

    # async def save_document(self: Self, doc_data: SaveDocumentSchema) -> Document:
    #     print("saved")
    #     return Document(owner=1, pages=None)

    # async def acquire_fields(self: Self, doc_data: AcquireFieldsDocuemtnSchema) -> Document:
    #     print("Fields acquired")
    #     return Document(owner=1, pages=None)

    # async def translate_document(self: Self, doc_data: TranslateDocumentSchema) -> Document:
    #     print("translated")
    #     return Document(owner=1, pages=None)


async def get_documents_use_case(document_factory: DocumentFactory) -> DocumentsUseCaseProtocol:
    return DocumentsUseCaseImpl(document_factory)


DocumentsUseCase = Annotated[DocumentsUseCaseProtocol, Depends(get_documents_use_case)]
