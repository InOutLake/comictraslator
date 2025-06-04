from enum import StrEnum, auto
from fastapi import Depends
from typing import Annotated, Protocol, Self
from shared.repositories.rmqrepository import RMQSendClient
from shared.settings import Settings, settings


class Default(StrEnum):
    DEFAULT = auto()


class LogsRepository(Protocol):
    async def send_logs(self: Self, record: str) -> None: ...


class LogsRepositoryRMQImpl(LogsRepository, RMQSendClient):
    def __init__(self: Self, settings: Settings):
        super().__init__(settings)
        self.exchage_name = self.settings.LOGS_EXCHANGE

    async def send_logs(self: Self, record: str) -> None:
        await self.send(Default.DEFAULT, record)


async def logs_repository_factory():
    repo = LogsRepositoryRMQImpl(settings)
    await repo.initialize()
    return repo


LogsRepositoryDep = Annotated[LogsRepository, Depends(logs_repository_factory)]
