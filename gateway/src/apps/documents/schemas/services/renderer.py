from typing import List
from pydantic import BaseModel
from gateway.src.apps.documents.schemas.services.documents import Frame


class RenderRequest(BaseModel):
    cleaned_url: str
    frames: List[Frame]


class RenderResponse(BaseModel):
    rendered_url: str
