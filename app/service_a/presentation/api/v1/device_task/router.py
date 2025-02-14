from fastapi import (
    APIRouter,
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
            Message(id=device_task.task_id),
        )
        # await asyncio.sleep(60)
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": exception.message},
        )
    return ProvisionResponseSchema(
        code=status.HTTP_200_OK,
        message=str(device_task.task_id),
    )
