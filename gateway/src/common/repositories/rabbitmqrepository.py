from enum import Enum
from typing import Self
import uuid

from pydantic import BaseModel
from src.common.settings import Settings
import aio_pika


class RabbitMQRepository:
    """
    ### Warning!
    Initialize before usage!
    ### Usage example:
    ```python
    async def read_document(self: Self, data: SomeSchema) -> Document:
        correlation_id = str(uuid.uuid4())
        future = asyncio.get_event_loop().create_future()
        self.futures[correlation_id] = future

        await self.publish_message(
                SomeEnum.SOMEACTION,
                data,
                correlation_id=correlation_id,
            )

        response = await future
        return Document.model_validate_json(response)
    ```
    """

    exchange_name: str = "default"

    def __init__(self: Self, settings: Settings) -> None:
        self.settings = settings
        self.connection: aio_pika.Connection | None = None
        self.channel: aio_pika.Channel | None = None
        self.callback_queue: aio_pika.Queue | None = None
        self.futures = {}

    async def publish_message(
        self: Self,
        action: Enum,
        data: BaseModel,
        correlation_id: uuid.UUID,
    ):
        await self.exchange.publish(
            aio_pika.Message(
                body=data.model_dump_json().encode(),
                reply_to=self.callback_queue.name,
                correlation_id=correlation_id,
                action=action,
            ),
            # routing key meant to be the same as exchange_name for now
            routing_key=self.exchange_name,
        )

    async def initialize(self: Self) -> None:
        self.connection = await aio_pika.connect_robust(
            host=self.settings.host,
            port=self.settings.port,
            login=self.settings.user,
            password=self.settings.password,
        )
        self.channel = await self.conneciton.channel()
        exchange = await self.channel.get_exchange(self.exchange_name)
        if not exchange:
            await self.channel.declare_exchange(self.exchange_name)
            exchange = await self.channel.get_exchange(self.exchange_name)
        self.exchange = exchange
        self.callback_queue = await self.channel.declare_queue(exclusive=True)
        await self.callback_queue.consume(self._on_response)

    async def _on_response(self: Self, message: aio_pika.IncomingMessage) -> None:
        async with message.process():
            correlation_id = message.correlation_id
            if correlation_id in self.futures:
                self.futures[correlation_id].set_result(message.body)
                del self.futures[correlation_id]


# def get_document_repository() -> DocumentsRepositoryProtocol: ...
