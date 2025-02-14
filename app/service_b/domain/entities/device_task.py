from dataclasses import (
    dataclass,
    field,
)
from datetime import datetime
from uuid import uuid4

from service_b.domain.entities.base import BaseEntity
from service_b.domain.value_objects.status import TaskStatus
from service_b.tools.time_utils import ts_now


@dataclass
class DeviceTask(BaseEntity):
    id: int | None = None
    task_id: str = field(default_factory=lambda: str(uuid4()))
    equipment_id: str | None = None
    parameters: dict | None = None
    status: int = field(default=TaskStatus.NOTHING.value)
    created_at: datetime = field(default_factory=ts_now)

    def validate(self) -> None: ...

    @classmethod
    def build(cls, equipment_id: str, parameters: dict) -> "DeviceTask":
        return cls(
            equipment_id=equipment_id,
            parameters=parameters,
        )
