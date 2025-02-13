import httpx
from faststream.rabbit import (
    RabbitQueue,
    RabbitRouter,
)
from httpx import Response

from infrastructure.message_broker.constants import DEVICE_TASK_QUEUE_NAME
from infrastructure.message_broker.message import Message as BrokerMessage
from settings.config import settings


router = RabbitRouter()


@router.subscriber(queue=RabbitQueue(name=DEVICE_TASK_QUEUE_NAME, durable=True))
async def handle_device_task(aio_message: dict) -> None:
    try:
        message: BrokerMessage = BrokerMessage(**aio_message)

        print(message)
        async with httpx.AsyncClient() as client:
            response: Response = await client.post(
                url=f"http://{settings.SERVICE_A_API_HOST}:{settings.SERVICE_A_API_PORT}/api/v1/equipment/cpe/{id}",
            )
            response.raise_for_status()
    except Exception as e:
        print(f"Error processing message: {e}")
