from dataclasses import dataclass
from time import sleep
from typing import Iterable

from service_a.domain.entities.device_task import DeviceTask
from service_a.domain.value_objects.status import TaskStatus
from service_a.infrastructure.exceptions.repository import DeviceTaskNotFoundException
from service_a.infrastructure.repositories.base import BaseDeviceTaskRepository
from sqlalchemy import (
    delete,
    select,
    update,
)
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session


@dataclass
class PostgreSQLDeviceTaskRepository(BaseDeviceTaskRepository):
    engine: Engine

    def add_task(self, task: DeviceTask) -> None:
        """
        Добавляет задачу в базу данных.
        """
        with Session(self.engine, expire_on_commit=False) as session:
            session.add(task)
            session.commit()

    def get_task_by_id(self, id: int) -> DeviceTask:
        """
        Получает задачу по её ID.
        Если задача не найдена, выбрасывает исключение DeviceTaskNotFoundException.
        """
        with Session(self.engine, expire_on_commit=False) as session:
            query = select(DeviceTask).where(DeviceTask.id == id)
            result = session.execute(query)
            task: DeviceTask | None = result.scalar_one_or_none()

            if not task:
                raise DeviceTaskNotFoundException()

            return task

    def get_all_task(self) -> Iterable[DeviceTask]:
        """
        Получает все задачи из базы данных.
        """
        with Session(self.engine, expire_on_commit=False) as session:
            query = select(DeviceTask)
            result = session.scalars(query)
            tasks: Iterable[DeviceTask] = result.all()
            return tasks

    def update_task_status_to_completed(
        self,
        equipment_id: str,
        task_id: str,
        delay: int = 0,
    ) -> None:
        """
        Обновляет статус задачи на выполненное.
        """

        sleep(delay)
        with Session(self.engine, expire_on_commit=False) as session:
            stmt = (
                update(DeviceTask)
                .where(
                    DeviceTask.equipment_id == equipment_id,
                    DeviceTask.task_id == task_id,
                )
                .values(status=TaskStatus.COMPLETED.value)
            )
            session.execute(stmt)
            session.commit()

    def delete_task_by_id(self, id: int) -> None:
        """
        Удаляет задачу по её ID.
        """
        with Session(self.engine, expire_on_commit=False) as session:
            query = delete(DeviceTask).where(DeviceTask.id == id)
            session.execute(query)
            session.commit()
