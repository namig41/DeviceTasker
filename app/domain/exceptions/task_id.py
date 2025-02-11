from dataclasses import dataclass

from domain.exceptions.base import ApplicationException


@dataclass(eq=False)
class EquipmentIdIncorrectValueException(ApplicationException):
    @property
    def message(self):
        return "Неверный серийный номер устройства"
