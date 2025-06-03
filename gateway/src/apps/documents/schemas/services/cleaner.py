from typing import List
from gateway.src.apps.documents.schemas.services.documents import Frame
from pydantic import BaseModel


class CleanRequest(BaseModel):
    page_url: str
    fields: List[Frame]


class CleanResponse(BaseModel):
    page_url: str
