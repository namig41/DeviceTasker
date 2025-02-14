from dataclasses import dataclass

from domain.exceptions.base import ApplicationException


@dataclass(eq=False)
class DeviceIdIncorrectValueException(ApplicationException):
    @property
    def message(self):
        return "Invalid serial number format"
