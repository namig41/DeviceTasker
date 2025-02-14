from service_b.infrastructure.message_broker.base import BaseMessageBroker
from service_b.infrastructure.message_broker.constants import (
    DEVICE_TASK_EXCHANGE_NAME,
    DEVICE_TASK_QUEUE_NAME,
    DEVICE_TASK_ROUTE_KEY_TEMPLATE,
)


async def configure_message_broker(message_broker: BaseMessageBroker) -> None:
    await message_broker.declare_exchange(DEVICE_TASK_EXCHANGE_NAME)
    await message_broker.declare_queue(
        DEVICE_TASK_QUEUE_NAME,
        DEVICE_TASK_EXCHANGE_NAME,
        DEVICE_TASK_ROUTE_KEY_TEMPLATE,
    )
