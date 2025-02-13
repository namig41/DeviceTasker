import re
from dataclasses import dataclass

from domain.exceptions.task_id import DeviceIdIncorrectValueException
from domain.value_objects.base import BaseValueObject


@dataclass(frozen=True)
class TaskID(BaseValueObject[str]):

    def validate(self) -> None:
        if bool(re.match(r"^[a-zA-Z0-9]{6,}$", self.value)):
            raise DeviceIdIncorrectValueException()
