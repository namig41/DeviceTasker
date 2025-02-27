from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    HTTPException,
    status,
)

from punq import Container
from service_b.bootstrap.di import init_container
from service_b.domain.entities.device_task import DeviceTask
from service_b.domain.exceptions.base import ApplicationException
from service_b.domain.value_objects.status import TaskStatus
from service_b.infrastructure.exceptions.repository import DeviceTaskNotFoundException
from service_b.infrastructure.message_broker.message import Message
from service_b.infrastructure.message_broker.producer.base import BaseProducer
from service_b.infrastructure.repositories.base import BaseDeviceTaskRepository
from service_b.presentation.api.v1.device_task.schemas import (
    DeviceTaskRequestSchema,
    ProvisionResponseSchema,
)


router = APIRouter(
    prefix="/api/v1/equipment/cpe",
    tags=["DeviceTask"],
)


@router.post(
    "/{equipment_id}",
    status_code=status.HTTP_200_OK,
    description="Device activation",
)
async def create_task(
    device_task_schema: DeviceTaskRequestSchema,
    equipment_id: str,
    background_tasks: BackgroundTasks,
    container: Container = Depends(init_container),
) -> ProvisionResponseSchema:
    try:
        repository: BaseDeviceTaskRepository = container.resolve(
            BaseDeviceTaskRepository,
        )
        producer: BaseProducer = container.resolve(BaseProducer)

        device_task: DeviceTask = DeviceTask.build(
            equipment_id=equipment_id,
            parameters=device_task_schema.parameters,
        )

        await repository.add_task(device_task)

        await producer.publish(
            Message(
                data={
                    "task_id": device_task.task_id,
                    "device_id": device_task.equipment_id,
                },
            ),
        )

        background_tasks.add_task(
            repository.update_task_status_to_completed,
            equipment_id=device_task.equipment_id,
            task_id=device_task.task_id,
            delay=device_task_schema.timeoutInSeconds,
        )

    except DeviceTaskNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "The requested equipment is not found"},
        )
    except ApplicationException:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Internal provisioning exception"},
        )
    return ProvisionResponseSchema(
        code=status.HTTP_200_OK,
        message=device_task.task_id,
    )


@router.get(
    "/{equipment_id}/task/{task_id}",
    status_code=status.HTTP_200_OK,
    description="Getting the device task status",
)
async def get_task_status(
    equipment_id: str,
    task_id: str,
    container: Container = Depends(init_container),
) -> ProvisionResponseSchema:
    try:
        repository: BaseDeviceTaskRepository = container.resolve(
            BaseDeviceTaskRepository,
        )

        device_task: DeviceTask = await repository.get_task_by_id(
            task_id=task_id,
            equipment_id=equipment_id,
        )

        if device_task.status == TaskStatus.COMPLETED.value:
            response: ProvisionResponseSchema = ProvisionResponseSchema(
                code=status.HTTP_200_OK,
                message="Completed",
            )
        elif device_task.status == TaskStatus.RUNNING.value:
            response: ProvisionResponseSchema = ProvisionResponseSchema(
                code=status.HTTP_204_NO_CONTENT,
                message="Task is still running",
            )
        else:
            raise ApplicationException()

    except DeviceTaskNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "The requested equipment is not found"},
        )
    except ApplicationException:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Internal provisioning exception"},
        )

    return response
