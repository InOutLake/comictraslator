import asyncio
from enum import Enum
from typing import Any, Self
import uuid

from pydantic import BaseModel
from shared.settings import Settings
import aio_pika


class RMQClientBase:
    exchange_name: str = "default"

    def __init__(self: Self, settings: Settings) -> None:
        self.settings = settings
        self.connection: aio_pika.abc.AbstractConnection | None = None
        self.channel: aio_pika.abc.AbstractChannel | None = None

    async def initialize(self: Self) -> None:
        self.connection = await aio_pika.connect(
            host=self.settings.RMQ_HOST,
            port=self.settings.RMQ_PORT,
            login=self.settings.RMQ_USER,
            password=self.settings.RMQ_PASS,
        )
        self.channel = await self.connection.channel()
        exchange = await self.channel.get_exchange(self.exchange_name)
        if not exchange:
            await self.channel.declare_exchange(self.exchange_name)
            exchange = await self.channel.get_exchange(self.exchange_name)
        self.exchange = exchange


class RMQSendClient(RMQClientBase):
    async def send(self: Self, message: Any):
        await self.exchange.publish(
            aio_pika.Message(bytes(message, "utf-8")),
            routing_key=self.exchange_name,
        )


class RMQRPCClient(RMQClientBase):
    """
    ### Warning!
    Initialize before usage!
    ### Usage example:
    ```python
    async def read_document(self: Self, data: SomeSchema) -> Document:
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
        self.callback_queue: aio_pika.abc.AbstractQueue | None = None
        self.futures = {}
        super().__init__(settings)

    async def do(
        self: Self,
        action: Enum,
        data: BaseModel,
    ):
        correlation_id = str(uuid.uuid4())
        future = asyncio.get_running_loop().create_future()
        self.futures[correlation_id] = future
        await self.exchange.publish(
            aio_pika.Message(
                body=data.model_dump_json().encode(),
                headers={"action": action.value},
                reply_to=self.callback_queue.name,  # type: ignore
                correlation_id=correlation_id,
            ),
            # routing key meant to be the same as exchange_name for now
            routing_key=self.exchange_name,
        )
        response = await future
        self.futures.pop(correlation_id)
        return response.body.decode()

    async def initialize(self: Self) -> None:
        await super().initialize()
        self.callback_queue = await self.channel.declare_queue(exclusive=True)  # type: ignore
        await self.callback_queue.consume(self._on_response)

    async def _on_response(
        self: Self, message: aio_pika.abc.AbstractIncomingMessage
    ) -> None:
        async with message.process():
            correlation_id = message.correlation_id
            if correlation_id in self.futures:
                self.futures[correlation_id].set_result(message.body)
                del self.futures[correlation_id]
