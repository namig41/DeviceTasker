from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass
from typing import Iterable

from service_a.domain.entities.device_task import DeviceTask


@dataclass
class BaseDeviceTaskRepository(ABC):

    @abstractmethod
    def add_task(self, task: DeviceTask) -> None: ...

    @abstractmethod
    def get_task_by_id(self, id: int) -> DeviceTask: ...

    @abstractmethod
    def get_all_task(self) -> Iterable[DeviceTask]: ...

    @abstractmethod
    def update_task_status_to_completed(
        self, equipment_id: str, task_id: str, delay: int,
    ) -> None: ...

    @abstractmethod
    def delete_task_by_id(self, id: int) -> None: ...
