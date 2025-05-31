from pydantic_settings.main import BaseSettings


class Settings(BaseSettings):
    RABBIT_CONNECTIONSTRING: str
