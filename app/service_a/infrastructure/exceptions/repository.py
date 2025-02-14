from dataclasses import dataclass

from service_a.infrastructure.exceptions.base import InfraException


@dataclass(eq=False)
class DeviceTaskNotFoundException(InfraException):
    @property
    def message(self):
        return "Задача не найдена"
