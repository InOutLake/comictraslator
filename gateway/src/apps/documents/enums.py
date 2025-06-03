from enum import StrEnum, auto


class OCRActions(StrEnum):
    FIND_AREAS = auto()
    GET_TEXT = auto()


class TranslateActions(StrEnum):
    TRANSLATE = auto()
