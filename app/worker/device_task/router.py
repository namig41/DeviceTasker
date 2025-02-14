import httpx
from faststream.rabbit import (
    RabbitQueue,
    RabbitRouter,
)
from httpx import Response
from worker.device_task.constants import DEVICE_TASK_QUEUE_NAME
from worker.device_task.message import Message as BrokerMessage
from worker.settings import settings


router = RabbitRouter()


@router.subscriber(queue=RabbitQueue(name=DEVICE_TASK_QUEUE_NAME, durable=True))
async def handle_device_task(aio_message: dict) -> None:
    try:
        message: BrokerMessage = BrokerMessage(**aio_message)

        print(message)
        async with httpx.AsyncClient(base_url=settings.get_service_url) as client:
            response: Response = await client.post(
                url=f"/api/v1/equipment/cpe/{id}",
            )
            response.raise_for_status()
    except Exception as e:
        print(f"Error processing message: {e}")
