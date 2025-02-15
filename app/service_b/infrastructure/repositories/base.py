from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass
from typing import Iterable

from service_b.domain.entities.device_task import DeviceTask


@dataclass
class BaseDeviceTaskRepository(ABC):

    @abstractmethod
    async def add_task(self, task: DeviceTask) -> None: ...

    @abstractmethod
    async def get_task_by_id(self, equipment_id: str, task_id: str) -> DeviceTask: ...

    @abstractmethod
    async def get_all_task(self) -> Iterable[DeviceTask]: ...

    @abstractmethod
    async def update_task_status_to_completed(
        self, equipment_id: str, task_id: str, delay: int,
    ) -> None: ...

    @abstractmethod
    async def delete_task(self, equipment_id: str, task_id: str) -> None: ...
