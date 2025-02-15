import pytest
from punq import Container
from service_b.domain.entities.device_task import DeviceTask
from service_b.domain.value_objects.status import TaskStatus
from service_b.infrastructure.exceptions.repository import DeviceTaskNotFoundException
from service_b.infrastructure.repositories.base import BaseDeviceTaskRepository


@pytest.mark.asyncio
async def test_add_and_get_task(container: Container):
    repository: BaseDeviceTaskRepository = container.resolve(BaseDeviceTaskRepository)

    task: DeviceTask = DeviceTask(equipment_id="test")

    await repository.add_task(task)

    returned_task: DeviceTask = await repository.get_task_by_id(
        equipment_id=task.equipment_id, task_id=task.task_id,
    )

    await repository.delete_task(equipment_id=task.equipment_id, task_id=task.task_id)

    assert task == returned_task


@pytest.mark.asyncio
async def test_get_all_tasks(container: Container):
    repository: BaseDeviceTaskRepository = container.resolve(BaseDeviceTaskRepository)

    task1: DeviceTask = DeviceTask(equipment_id="test1")
    task2: DeviceTask = DeviceTask(equipment_id="test2")

    await repository.add_task(task1)
    await repository.add_task(task2)

    all_tasks = await repository.get_all_task()

    assert len(all_tasks) == 2
    assert task1 in all_tasks
    assert task2 in all_tasks

    await repository.delete_task(equipment_id=task1.equipment_id, task_id=task1.task_id)
    await repository.delete_task(equipment_id=task2.equipment_id, task_id=task2.task_id)


@pytest.mark.asyncio
async def test_update_task_status_to_completed(container: Container):
    repository: BaseDeviceTaskRepository = container.resolve(BaseDeviceTaskRepository)

    task: DeviceTask = DeviceTask(equipment_id="test")

    await repository.add_task(task)

    await repository.update_task_status_to_completed(
        equipment_id="test", task_id=task.task_id, delay=5,
    )

    updated_task: DeviceTask = await repository.get_task_by_id(
        equipment_id=task.equipment_id, task_id=task.task_id,
    )

    assert updated_task.status == TaskStatus.COMPLETED.value

    await repository.delete_task(equipment_id=task.equipment_id, task_id=task.task_id)


@pytest.mark.asyncio
async def test_delete_task(container: Container):
    repository: BaseDeviceTaskRepository = container.resolve(BaseDeviceTaskRepository)

    task: DeviceTask = DeviceTask(equipment_id="test")

    await repository.add_task(task)

    await repository.delete_task(equipment_id=task.equipment_id, task_id=task.task_id)

    with pytest.raises(DeviceTaskNotFoundException):
        await repository.get_task_by_id(equipment_id="test", task_id=task.task_id)


@pytest.mark.asyncio
async def test_task_not_found(container: Container):
    repository: BaseDeviceTaskRepository = container.resolve(BaseDeviceTaskRepository)

    with pytest.raises(DeviceTaskNotFoundException):
        await repository.get_task_by_id(equipment_id="nonexistent", task_id="999")
