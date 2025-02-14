import asyncio

from faststream.rabbit import RabbitBroker
from worker.device_task.router import router as device_task_router
from worker.settings import settings


async def run_consumer() -> None:
    broker: RabbitBroker = RabbitBroker(
        url=settings.get_message_broker_url,
    )

    broker.include_router(router=device_task_router)

    await broker.start()


if __name__ == "__main__":
    asyncio.run(run_consumer())
