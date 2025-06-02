from pydantic import BaseModel
from typing import Any, List


# TODO language enum
class Frame(BaseModel):
    start_cords: List[int]
    end_cords: List[int]
    text: str | None
    text_params: Any | None


class FrameTranslation(Frame):
    frame: Frame | None
    language: str


class Page(BaseModel):
    number: int
    frames: List[Frame]
    original_url: str
    cleared_url: str | None


class PageTranlsation(BaseModel):
    page: Page
    translatioin_url: str


class Document(BaseModel):
    owner: int
    name: str
    author: str
    orig_lang: str
    pages: List[Page] | None
