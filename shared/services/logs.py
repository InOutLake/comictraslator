from typing import Annotated, Self
from shared.repositories.logs import LogsRepository, LogsRepositoryDep
from shared.settings import settings
from fastapi import Depends
import logging
import asyncio


class RabbitMQHandler(logging.Handler):
    def __init__(self: Self, repo: LogsRepository):
        super().__init__()
        self.settings = settings
        self.repo = repo

    def emit(self: Self, record: logging.LogRecord) -> None:
        asyncio.run(self.repo.send_logs(self.format(record)))


def rabbit_mq_handler_factory(logs_repo: LogsRepositoryDep):
    return RabbitMQHandler(logs_repo)


RabbitMQHandlerDep = Annotated[RabbitMQHandler, Depends(rabbit_mq_handler_factory)]
