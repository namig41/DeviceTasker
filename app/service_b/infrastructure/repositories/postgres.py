from dataclasses import dataclass
from typing import Iterable

from service_b.domain.entities.device_task import DeviceTask
from service_b.infrastructure.exceptions.repository import DeviceTaskNotFoundException
from service_b.infrastructure.repositories.base import BaseDeviceTaskRepository
from sqlalchemy import (
    and_,
    delete,
    select,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio.engine import AsyncEngine


@dataclass
class PostgreSQLDeviceTaskRepository(BaseDeviceTaskRepository):

    engine: AsyncEngine

    async def add_task(self, task: DeviceTask) -> None:
        async with AsyncSession(self.engine, expire_on_commit=False) as session:
            session.add(task)
            await session.commit()

    async def get_task_by_id(self, equipment_id: str, task_id: str) -> DeviceTask:
        async with AsyncSession(self.engine, expire_on_commit=False) as session:
            query = select(DeviceTask).where(
                and_(
                    DeviceTask.task_id == task_id,
                    DeviceTask.equipment_id == equipment_id,
                ),
            )
            result = await session.execute(query)
            task: DeviceTask | None = result.scalar_one_or_none()

            if not task:
                raise DeviceTaskNotFoundException()

            return task

    async def get_all_task(self) -> Iterable[DeviceTask]:
        async with AsyncSession(self.engine, expire_on_commit=False) as session:
            query = select(DeviceTask)
            result = await session.scalars(query)
            users: Iterable[DeviceTask] = result.all()
            return users

    async def delete_task_by_id(self, id: int) -> None:
        async with AsyncSession(self.engine, expire_on_commit=False) as session:
            query = delete(DeviceTask).where(DeviceTask.id == id)
            await session.execute(query)
            await session.commit()
