from dataclasses import (
    dataclass,
    field,
)
from datetime import datetime
from uuid import uuid4

from tools.time_utils import ts_now

from domain.entities.base import BaseEntity
from domain.value_objects.status import TaskStatus


@dataclass
class Task(BaseEntity):
    id: int | None = None
    task_id: str = field(default_factory=lambda: str(uuid4()))
    equipment_id: str | None = None
    parameters: dict | None = None
    status: str = field(default=TaskStatus.RUNNING.value)
    created_at: datetime = field(default_factory=ts_now)

    def validate(self) -> None: ...
