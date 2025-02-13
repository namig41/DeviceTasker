import asyncio

from faststream.rabbit import RabbitBroker

from infrastructure.message_broker.config import MessageBrokerConfig
from presentation.consumer.device_task.router import router as device_task_router


async def run_consumer() -> None:
    message_broker_config: MessageBrokerConfig = MessageBrokerConfig()
    broker: RabbitBroker = RabbitBroker(
        url=message_broker_config.get_url,
    )

    broker.include_router(router=device_task_router)

    await broker.start()


if __name__ == "__main__":
    asyncio.run(run_consumer())
