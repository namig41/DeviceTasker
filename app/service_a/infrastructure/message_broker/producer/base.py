from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass

from service_a.infrastructure.message_broker.base import BaseMessageBroker
from service_a.infrastructure.message_broker.message import Message


@dataclass
class BaseProducer(ABC):
    message_broker: BaseMessageBroker

    @abstractmethod
    def publish(self, message: Message) -> None: ...
