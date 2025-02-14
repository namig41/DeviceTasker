from dataclasses import dataclass

from service_a.infrastructure.exceptions.base import InfraException


@dataclass(eq=False)
class DatabaseRunFailedException(InfraException):
    @property
    def message(self):
        return "Ошибка инициализации базы данных"
