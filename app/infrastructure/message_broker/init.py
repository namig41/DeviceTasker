from infrastructure.message_broker.base import BaseMessageBroker
from infrastructure.message_broker.constants import (
    TASK_EXCHANGE_NAME,
    TASK_QUEUE_NAME,
    TASK_ROUTE_KEY_TEMPLATE,
)


async def configure_message_broker(message_broker: BaseMessageBroker) -> None:
    await message_broker.declare_exchange(TASK_EXCHANGE_NAME)
    await message_broker.declare_queue(
        TASK_EXCHANGE_NAME,
        TASK_QUEUE_NAME,
        TASK_ROUTE_KEY_TEMPLATE,
    )
