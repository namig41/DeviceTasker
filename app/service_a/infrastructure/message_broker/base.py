from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass

from pika.abc import AbstractQueue

from infrastructure.message_broker.message import Message
from infrastructure.message_broker.message_broker_factory import ConnectionFactory


@dataclass
class BaseMessageBroker(ABC):
    connection_factory: ConnectionFactory

    @abstractmethod
    def publish_message(
        self,
        message: Message,
        routing_key: str,
        exchange_name: str,
    ) -> None: ...

    @abstractmethod
    def declare_exchange(self, exchange_name: str) -> None: ...

    @abstractmethod
    def declare_queue(
        self,
        queue_name: str,
        exchange_name: str,
        routing_key: str,
    ) -> AbstractQueue: ...

    @abstractmethod
    def connect(self) -> None: ...

    @abstractmethod
    def close(self) -> None: ...
