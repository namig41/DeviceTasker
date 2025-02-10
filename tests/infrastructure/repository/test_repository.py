import pytest
from punq import Container

from domain.entities.task import Task
from infrastructure.exceptions.repository import TaskNotFoundException
from infrastructure.repositories.base import BaseTaskRepository


@pytest.mark.asyncio
async def test_task_repository(container: Container):
    repository: BaseTaskRepository = container.resolve(BaseTaskRepository)

    task: Task = Task(id=1, equipment_id="test")

    await repository.add_task(task)

    returned_task: Task = await repository.get_task_by_id(id=1)

    assert task == returned_task

    await repository.delete_task_by_id(id=1)

    with pytest.raises(TaskNotFoundException):
        await repository.get_task_by_id(id=1)
