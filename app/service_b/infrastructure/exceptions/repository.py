from dataclasses import dataclass

from service_b.infrastructure.exceptions.base import InfraException


@dataclass(eq=False)
class DeviceTaskNotFoundException(InfraException):
    @property
    def message(self):
        return "Задача не найдена"
