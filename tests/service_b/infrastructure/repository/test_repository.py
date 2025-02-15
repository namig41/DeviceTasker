import pytest
from punq import Container
from service_b.domain.entities.device_task import DeviceTask
from service_b.infrastructure.exceptions.repository import DeviceTaskNotFoundException
from service_b.infrastructure.repositories.base import BaseDeviceTaskRepository


@pytest.mark.asyncio
async def test_task_repository(container: Container):
    repository: BaseDeviceTaskRepository = container.resolve(BaseDeviceTaskRepository)

    task: DeviceTask = DeviceTask(id=1, equipment_id="test")

    await repository.add_task(task)

    returned_task: DeviceTask = await repository.get_task_by_id(id=1)

    assert task == returned_task

    await repository.delete_task_by_id(id=1)

    with pytest.raises(DeviceTaskNotFoundException):
        await repository.get_task_by_id(id=1)
