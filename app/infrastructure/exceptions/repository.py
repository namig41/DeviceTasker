from dataclasses import dataclass

from infrastructure.exceptions.base import InfraException


@dataclass(eq=False)
class TaskNotFoundException(InfraException):
    @property
    def message(self):
        return "Задача не найдена"
