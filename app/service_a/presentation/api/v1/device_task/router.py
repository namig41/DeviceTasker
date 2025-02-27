from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    HTTPException,
    status,
)

from punq import Container
from service_a.bootstrap.di import init_container
from service_a.domain.entities.device_task import DeviceTask
from service_a.domain.exceptions.base import ApplicationException
from service_a.infrastructure.message_broker.message import Message
from service_a.infrastructure.message_broker.producer.base import BaseProducer
from service_a.infrastructure.repositories.base import BaseDeviceTaskRepository
from service_a.presentation.api.v1.device_task.schemas import (
    DeviceTaskRequestSchema,
    ProvisionResponseSchema,
)
from service_b.infrastructure.exceptions.repository import DeviceTaskNotFoundException


router = APIRouter(
    prefix="/api/v1/equipment/cpe",
    tags=["DeviceTask"],
)


@router.post(
    "/{equipment_id}",
    status_code=status.HTTP_200_OK,
    description="Device activation",
)
def create_task(
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

        repository.add_task(device_task)

        producer.publish(
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
