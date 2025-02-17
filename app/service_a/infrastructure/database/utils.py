from service_a.domain.entities.device_task import DeviceTask
from service_a.infrastructure.database.models import (
    mapper_registry,
    metadata,
    tasks,
)


def start_entity_mappers() -> None:
    mapper_registry.map_imperatively(DeviceTask, tasks)
