from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass

from aio_pika.abc import AbstractQueue
from service_b.infrastructure.message_broker.message import Message
from service_b.infrastructure.message_broker.message_broker_factory import ConnectionFactory


@dataclass
class BaseMessageBroker(ABC):
    connection_factory: ConnectionFactory

    @abstractmethod
    async def publish_message(
        self,
        message: Message,
        routing_key: str,
        exchange_name: str,
    ) -> None: ...

    @abstractmethod
    async def declare_exchange(self, exchange_name: str) -> None: ...

    @abstractmethod
    async def declare_queue(
        self,
        queue_name: str,
        exchange_name: str,
        routing_key: str,
    ) -> AbstractQueue: ...

    @abstractmethod
    async def connect(self) -> None: ...

    @abstractmethod
    async def close(self) -> None: ...
