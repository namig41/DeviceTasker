import asyncio

import pytest
from punq import Container

from infrastructure.message_broker.base import BaseMessageBroker
from infrastructure.message_broker.message import Message


@pytest.mark.asyncio
async def test_message_broker_with_factory(container: Container):
    message_broker: BaseMessageBroker = container.resolve(BaseMessageBroker)
    await message_broker.connect()

    # Объявляем обменник
    exchange_name: str = "test_exchange"
    await message_broker.declare_exchange(exchange_name)

    await message_broker.declare_queue("my_queue", exchange_name, "test.*")

    # Публикуем сообщение
    message = Message(message_type="example", data={"key": "value"})
    routing_key: str = "test.key"
    for _ in range(10):
        await message_broker.publish_message(message, routing_key, exchange_name)
        await asyncio.sleep(1)

    await message_broker.close()
