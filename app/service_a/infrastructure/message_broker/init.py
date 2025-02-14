from service_a.infrastructure.message_broker.base import BaseMessageBroker
from service_a.infrastructure.message_broker.constants import (
    DEVICE_TASK_EXCHANGE_NAME,
    DEVICE_TASK_QUEUE_NAME,
    DEVICE_TASK_ROUTE_KEY_TEMPLATE,
)


def configure_message_broker(message_broker: BaseMessageBroker) -> None:
    message_broker.declare_exchange(DEVICE_TASK_EXCHANGE_NAME)
    message_broker.declare_queue(
        DEVICE_TASK_QUEUE_NAME,
        DEVICE_TASK_EXCHANGE_NAME,
        DEVICE_TASK_ROUTE_KEY_TEMPLATE,
    )
