import logging

import httpx
from faststream.rabbit import (
    RabbitQueue,
    RabbitRouter,
)
from httpx import Response
from worker.device_task.constants import (
    DEVICE_TASK_QUEUE_A_NAME,
    DEVICE_TASK_QUEUE_B_NAME,
)
from worker.settings import settings


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = RabbitRouter()

cert_path = "/etc/ssl/ssl.crt"


async def process_device_task(aio_message: dict, endpoint: str) -> None:
    try:
        logger.info(f"Received message: {aio_message}")

        device_id: str = aio_message["data"]["device_id"]
        task_id: str = aio_message["data"]["task_id"]

        async with httpx.AsyncClient(
            base_url=settings.get_service_url, verify=False,
        ) as client:
            url: str = endpoint.format(device_id=device_id, task_id=task_id)
            response: Response = await client.get(url)
            response.raise_for_status()

            result = response.json()
            logger.info(f"Status is: {result['message']}")

        logger.info(f"Successfully processed message: {aio_message}")
    except Exception as e:
        logger.error(f"Error processing message: {e}", exc_info=True)


@router.subscriber(queue=RabbitQueue(name=DEVICE_TASK_QUEUE_A_NAME, durable=True))
async def handle_device_task_service_a(aio_message: dict) -> None:
    await process_device_task(
        aio_message,
        "/api/v1/equipment/cpe/{device_id}/task/{task_id}",
    )


@router.subscriber(queue=RabbitQueue(name=DEVICE_TASK_QUEUE_B_NAME, durable=True))
async def handle_device_task_service_b(aio_message: dict) -> None:
    await process_device_task(
        aio_message,
        "/api/v1/equipment/cpe/{device_id}/task/{task_id}",
    )
