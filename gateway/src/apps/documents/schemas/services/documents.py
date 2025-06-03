from apps.documents.enums import Languages
from pydantic import BaseModel
from typing import Any, List


class Frame(BaseModel):
    start_cords: List[int]
    end_cords: List[int]
    text: str | None
    text_params: Any | None = None


class Page(BaseModel):
    number: int
    frames: List[Frame] | None = None
    original_url: str
    cleared_url: str | None


class PageTranlsation(BaseModel):
    page: Page
    translatioin_url: str
    language: Languages


class TranslatedFrame(BaseModel):
    language: Languages
    parent_frame: Frame | None = None
    frame: Frame
    page_translation: PageTranlsation


class Document(BaseModel):
    owner: int
    name: str
    author: str
    orig_lang: str
    pages: List[Page] | None
