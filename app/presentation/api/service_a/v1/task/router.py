import asyncio

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from punq import Container

from bootstrap.di import init_container
from domain.exceptions.base import ApplicationException
from infrastructure.repositories.base import BaseDeviceTaskRepository
from presentation.api.service_a.v1.task.schemas import (
    DeviceTaskRequestSchema,
    ProvisionResponseSchema,
)


router = APIRouter(
    prefix="/api/v1/equipment/cpe",
    tags=["Task"],
)


@router.post(
    "/{equipment_id}",
    status_code=status.HTTP_200_OK,
    description="Инициализация устройства",
)
async def initialize_device(
    device_task: DeviceTaskRequestSchema,
    equipment_id: int = Depends(),
    container: Container = Depends(init_container),
) -> ProvisionResponseSchema:
    try:
        repository: BaseDeviceTaskRepository = container.resolve(
            BaseDeviceTaskRepository,
        )
        await repository.get_task_by_id(equipment_id)

        await asyncio.sleep(60)
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": exception.message},
        )
    return ProvisionResponseSchema(code=status.HTTP_200_OK, message="success")
