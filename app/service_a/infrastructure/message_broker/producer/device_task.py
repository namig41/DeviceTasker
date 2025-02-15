from service_a.infrastructure.message_broker.constants import (
    DEVICE_TASK_EXCHANGE_NAME,
    DEVICE_TASK_ROUTE_KEY_TEMPLATE,
)
from service_a.infrastructure.message_broker.message import Message
from service_a.infrastructure.message_broker.producer.base import BaseProducer


class DeviceTaskProducer(BaseProducer):
    def publish(self, message: Message) -> None:
        self.message_broker.publish_message(
            message,
            DEVICE_TASK_ROUTE_KEY_TEMPLATE,
            DEVICE_TASK_EXCHANGE_NAME,
        )
