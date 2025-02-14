from service_a.domain.entities.device_task import DeviceTask
from service_a.infrastructure.database.models import (
    mapper_registry,
    metadata,
    tasks,
)
from sqlalchemy.ext.asyncio import AsyncEngine


def start_entity_mappers() -> None:
    mapper_registry.map_imperatively(DeviceTask, tasks)


async def create_database(engine: AsyncEngine) -> None:
    async with engine.begin() as connection:
        await connection.run_sync(metadata.create_all)


async def drop_database(engine: AsyncEngine) -> None:
    async with engine.begin() as connection:
        await connection.run_sync(metadata.drop_all)
