from enum import StrEnum, auto


class Languages(StrEnum):
    RUS = auto()
    JPN = auto()


class CleanerActions(StrEnum):
    CLEAN = auto()


class OCRActions(StrEnum):
    FIND_AREAS = auto()
    GET_TEXT = auto()


class TranslateActions(StrEnum):
    TRANSLATE = auto()
