from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass
from typing import Iterable

from domain.entities.task import Task


@dataclass
class BaseTaskRepository(ABC):

    @abstractmethod
    async def add_task(self, task: Task) -> None: ...

    @abstractmethod
    async def get_task_by_id(self, id: int) -> Task: ...

    @abstractmethod
    async def get_all_task(self) -> Iterable[Task]: ...

    @abstractmethod
    async def delete_task_by_id(self, id: int) -> None: ...
