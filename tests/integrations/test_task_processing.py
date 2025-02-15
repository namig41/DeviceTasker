import asyncio

import pytest
from httpx import AsyncClient
from punq import Container
from service_b.domain.value_objects.status import TaskStatus
from service_b.infrastructure.repositories.base import BaseDeviceTaskRepository


@pytest.mark.asyncio
async def test_task_processing(
    container: Container,
    service_a_client: AsyncClient,
    service_b_client: AsyncClient,
):
    repository: BaseDeviceTaskRepository = container.resolve(BaseDeviceTaskRepository)

    equipment_id = "1234"
    payload = {"timeoutInSeconds": 10, "parameters": {}}

    response = service_b_client.post(
        f"/api/v1/equipment/cpe/{equipment_id}",
        json=payload,
    )

    assert response.status_code == 200
    assert response.json() == {"message": equipment_id}

    response = service_b_client.post(
        "/api/v1/tasks/",
        json={"equipment_id": "device_1"},
    )
    assert response.status_code == 201
    task_id = response.json()["task_id"]

    task = await repository.get_task_by_id(equipment_id="device_1", task_id=task_id)
    assert task is not None
    assert task.status == TaskStatus.RUNNING.value

    await asyncio.sleep(2)

    updated_task = await repository.get_task_by_id(
        equipment_id="device_1", task_id=task_id,
    )
    assert updated_task.status == TaskStatus.COMPLETED.value

    repository.delete_task(
        equipment_id=updated_task.equipment_id,
        task_id=updated_task.task_id,
    )
