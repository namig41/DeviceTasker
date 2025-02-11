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
from infrastructure.repositories.base import BaseTaskRepository
from presentation.api.service_b.v1.task.schemas import (
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
async def create_task(
    device_task: DeviceTaskRequestSchema,
    equipment_id: int = Depends(),
    container: Container = Depends(init_container()),
) -> ProvisionResponseSchema:
    try:
        repository: BaseTaskRepository = container.resolve(BaseTaskRepository)
        await repository.get_task_by_id(equipment_id)

        await asyncio.sleep(60)
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": exception.message},
        )
    return ProvisionResponseSchema(code=status.HTTP_200_OK, message="success")


@router.get(
    "{equipment_id}/task/{task_id}",
    status_code=status.HTTP_200_OK,
    description="Инициализация устройства",
)
async def get_task_status(
    equipment_id: str,
    task_id: str,
    container: Container = Depends(init_container()),
) -> ProvisionResponseSchema:
    try:
        repository: BaseTaskRepository = container.resolve(BaseTaskRepository)
        await repository.get_task_by_id(equipment_id)
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": exception.message},
        )

    return ProvisionResponseSchema(code=status.HTTP_200_OK, message="success")
