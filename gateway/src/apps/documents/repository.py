from typing import Annotated, Any, Self, Protocol
from pydantic import BaseModel

from src.tools.settings import Settings
from src.apps.documents.schemas import Document, DBDocumentSchema
from src.apps.documents.enums import DocumentsActionsEnum
import asyncio
import aio_pika
import uuid


class DocumentsRepositoryProtocol(Protocol):
    async def read_document(self: Self, document_data: DBDocumentSchema) -> Document: ...


class DocumentsRabbitMQRepository:
    def __init__(self: Self, settings: Settings) -> None:
        self.rmqconfig = settings.config["RABBITMQ"]
        self.connection: aio_pika.Connection | None = None
        self.channel: aio_pika.Channel | None = None
        self.callback_queue: aio_pika.Queue | None = None
        self.futures = {}

    async def publish_message(
        self: Self,
        action: DocumentsActionsEnum,
        document_data: BaseModel,
        correlation_id: uuid.UUID,
    ):
        await self.documents_exchange.publish(
            aio_pika.Message(
                body=document_data.model_dump_json().encode(),
                reply_to=self.callback_queue.name,
                correlation_id=correlation_id,
                action=action,
            ),
            routing_key="documents",
        )

    async def initialize(self: Self) -> None:
        self.connection = await aio_pika.connect_robust(
            host=self.rmqconfig["host"],
            port=self.rmqconfig["port"],
            login=self.rmqconfig["user"],
            password=self.rmqconfig["password"],
        )
        self.channel = await self.conneciton.channel()
        exchange = await self.channel.get_exchange("documents")
        if not exchange:
            await self.channel.declare_exchange("documents")
            exchange = await self.channel.get_exchange("documents")
        self.documents_exchange = exchange
        self.callback_queue = await self.channel.declare_queue(exclusive=True)
        await self.callback_queue.consume(self._on_response)

    async def _on_response(self: Self, message: aio_pika.IncomingMessage) -> None:
        async with message.process():
            correlation_id = message.correlation_id
            if correlation_id in self.futures:
                self.futures[correlation_id].set_result(message.body)
                del self.futures[correlation_id]

    async def read_document(self: Self, document_data: DBDocumentSchema) -> Document:
        correlation_id = str(uuid.uuid4())
        future = asyncio.get_event_loop().create_future()
        self.futures[correlation_id] = future

        await self.publish_message(
            aio_pika.Message(
                body=document_data.model_dump_json().encode(),
                reply_to=self.callback_queue.name,
                correlation_id=correlation_id,
                action="read_document",
            ),
            routing_key="documents",
        )

        response = await future
        return Document.model_validate_json(response)


def get_document_repository() -> DocumentsRepositoryProtocol: ...
