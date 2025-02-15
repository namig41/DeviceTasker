from datetime import datetime

from faker import Faker
from service_b.domain.entities.device_task import DeviceTask
from service_b.domain.value_objects.status import TaskStatus


def test_create_task(faker: Faker):
    id: int = faker.pyint()
    task_id: str = faker.uuid4()
    equipment_id: str | None = None
    parameters: dict = {
        "parameters": {
            "username": "admin",
            "password": "admin",
            "vlan": 534,
            "interfaces": [1, 2, 3, 4],
        },
    }

    task: DeviceTask = DeviceTask(
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
    assert task.status == TaskStatus.NOTHING.value
