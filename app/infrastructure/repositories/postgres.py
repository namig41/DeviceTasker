from dataclasses import dataclass
from typing import Iterable

from sqlalchemy import (
    delete,
    select,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from domain.entities.task import Task
from infrastructure.exceptions.repository import TaskNotFoundException
from infrastructure.repositories.base import BaseTaskRepository


@dataclass
class PostgreSQLTaskRepository(BaseTaskRepository):

    engine: AsyncEngine

    async def add_task(self, task: Task) -> None:
        async with AsyncSession(self.engine, expire_on_commit=False) as session:
            session.add(task)
            await session.commit()

    async def get_task_by_id(self, id: int) -> Task:
        async with AsyncSession(self.engine, expire_on_commit=False) as session:
            query = select(Task).where(Task.id == id)
            result = await session.execute(query)
            task: Task | None = result.scalar_one_or_none()

            if not task:
                raise TaskNotFoundException()

            return task

    async def get_all_task(self) -> Iterable[Task]:
        async with AsyncSession(self.engine, expire_on_commit=False) as session:
            query = select(Task)
            result = await session.scalars(query)
            users: Iterable[Task] = result.all()
            return users

    async def delete_task_by_id(self, id: int) -> None:
        async with AsyncSession(self.engine, expire_on_commit=False) as session:
            query = delete(Task).where(Task.id == id)
            await session.execute(query)
            await session.commit()
