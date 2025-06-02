from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    RMQ_HOST: str
    RMQ_PORT: str
    RMQ_USER: str
    RMQ_PASS: str


settings = Settings(BaseSettings)
