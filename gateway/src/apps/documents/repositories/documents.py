from typing import Self, Protocol
from gateway.src.common.settings import settings
from src.apps.documents.schemas import Document, DBDocumentSchema


class DocumentsRepositoryProtocol(Protocol):
    async def read_document(
        self: Self, document_data: DBDocumentSchema
    ) -> Document: ...
