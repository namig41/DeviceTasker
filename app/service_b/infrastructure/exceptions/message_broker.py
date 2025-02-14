from dataclasses import dataclass

from service_b.infrastructure.exceptions.base import InfraException


@dataclass(eq=False)
class MessageBrokerFailedConnectionException(InfraException):
    @property
    def message(self):
        return "Ошибка подключения к брокеру сообщений"
