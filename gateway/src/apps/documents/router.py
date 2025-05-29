from fastapi import APIRouter

from src.apps.documents.schemas import Document, DBDocumentFilterSchema
from src.apps.documents.use_cases import DocumentsUseCase

router = APIRouter(tags=["Documents"], prefix="document")


@router.get("/")
async def list_documents(document_data: DBDocumentFilterSchema, document_use_case: DocumentsUseCase) -> Document:
    return await document_use_case.list_documents(document_data)


# @router.post("/save_document")
# async def save_document(document_data: SaveDocumentSchema, document_use_case: DocumentsUseCase) -> Document:
#     return await document_use_case.save_document(document_data)


# @router.post("/aquire_fields")
# async def aquire_fields(document_data: AquireFieldsDocumentSchema, document_use_case: DocumentsUseCase) -> Document:
#     return await document_use_case(document_data)
