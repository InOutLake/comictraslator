from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    RMQ_HOST: str = "default"
    RMQ_PORT: int = 0
    RMQ_USER: str = "default"
    RMQ_PASS: str = "default"

    S3_BUCKET_NAME: str = "default"
    S3_ENDPOINT_URL: str = "default"
    S3_ACCESS_KEY: str = "default"
    S3_SECRET_KEY: str = "default"

    LOGS_EXCHANGE: str = "default"


settings = Settings()
