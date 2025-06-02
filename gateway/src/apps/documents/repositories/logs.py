from typing import Protocol, Self
from gateway.src.common.repositories.rmqrepository import RMQSendClient


class LogsRepository(Protocol):
    async def send_logs(self: Self, message: str): ...


class OCRRabbitMQRepository(LogsRepository, RMQSendClient):
    exchange_name = "LOG"

    async def send_logs(self: Self, message: str):
        await self.send(message)
