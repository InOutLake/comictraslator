from tkinter import Frame
from typing import List
from pydantic import BaseModel


class FindAreasRequest(BaseModel): ...


class FindAreasResponse(BaseModel): ...


class TranslatePageKnownAreasRequest(BaseModel):
    frames: List[Frame]


class TranslatePageResponse(BaseModel):
    translated_url: str
