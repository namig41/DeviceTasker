from service_b.infrastructure.message_broker.constants import (
    DEVICE_TASK_EXCHANGE_NAME,
    DEVICE_TASK_ROUTE_KEY_TEMPLATE,
)
from service_b.infrastructure.message_broker.message import Message
from service_b.infrastructure.message_broker.producer.base import BaseProducer


class DeviceTaskProducer(BaseProducer):
    async def publish(self, message: Message) -> None:
        await self.message_broker.publish_message(
            message,
            DEVICE_TASK_ROUTE_KEY_TEMPLATE,
            DEVICE_TASK_EXCHANGE_NAME,
        )
