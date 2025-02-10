from datetime import datetime

from faker import Faker

from domain.entities.task import Task
from domain.value_objects.status import TaskStatus


def test_create_task(faker: Faker):
    id: int = faker.pyint()
    task_id: str = faker.uuid4()
    equipment_id: str | None = None
    parameters: dict = {}

    task: Task = Task(
        id=id,
        task_id=task_id,
        equipment_id=equipment_id,
        parameters=parameters,
    )

    assert task.id == id
    assert task.task_id == task_id
    assert task.equipment_id == equipment_id
    assert task.parameters == parameters
    assert isinstance(task.created_at, datetime)
    assert task.status == TaskStatus.RUNNING.value
