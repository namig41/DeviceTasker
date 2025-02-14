from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass
from typing import Any

from service_a.infrastructure.message_broker.message import Message
from service_a.infrastructure.message_broker.message_broker_factory import ConnectionFactory


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
    ) -> Any: ...

    @abstractmethod
    def connect(self) -> None: ...

    @abstractmethod
    def close(self) -> None: ...
