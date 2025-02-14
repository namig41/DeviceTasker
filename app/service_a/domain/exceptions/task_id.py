from dataclasses import dataclass

from service_a.domain.exceptions.base import ApplicationException


@dataclass(eq=False)
class DeviceIdIncorrectValueException(ApplicationException):
    @property
    def message(self):
        return "Invalid serial number format"
