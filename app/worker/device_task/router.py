import logging

import httpx
from faststream.rabbit import (
    RabbitQueue,
    RabbitRouter,
)
from httpx import Response
from worker.device_task.constants import DEVICE_TASK_QUEUE_NAME
from worker.settings import settings


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = RabbitRouter()


@router.subscriber(queue=RabbitQueue(name=DEVICE_TASK_QUEUE_NAME, durable=True))
async def handle_device_task(aio_message: dict) -> None:
    try:
        logger.info(f"Received message: {aio_message}")

        device_id: str = aio_message["data"]["device_id"]
        async with httpx.AsyncClient(base_url=settings.get_service_url) as client:
            response: Response = await client.post(
                url=f"/api/v1/equipment/cpe/{device_id}",
            )
            response.raise_for_status()

        logger.info(f"Successfully processed message: {aio_message}")
    except Exception as e:
        logger.error(f"Error processing message: {e}", exc_info=True)
