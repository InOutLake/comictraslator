from pydantic import BaseModel


class FindAreasResponse(BaseModel):
    response: str


class GetTextResponse(BaseModel):
    reponse: str
