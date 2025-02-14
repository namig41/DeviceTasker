from dataclasses import dataclass

from service_b.infrastructure.exceptions.base import InfraException


@dataclass(eq=False)
class DatabaseRunFailedException(InfraException):
    @property
    def message(self):
        return "Ошибка инициализации базы данных"
