from pydantic import BaseModel, PastDatetime
from typing import List


class Frame(BaseModel):
    start_cords: List[int]
    end_cords: List[int]
    original: str | None
    translated: str | None


class Page(BaseModel):
    number: int
    frames: List[Frame]


class Document(BaseModel):
    owner: int
    name: str
    author: str

    pages: List[Page] | None
    original_url: str
    cleared_url: str | None
    translated_url: str | None


class DBDocumentSchema(Document):
    id: int
    created_at: PastDatetime
    updated_at: PastDatetime


class DBDocumentFilterSchema:
    owner: int | None
    name: str | None
    author: str | None
