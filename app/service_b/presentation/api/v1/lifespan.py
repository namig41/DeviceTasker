from contextlib import asynccontextmanager

from fastapi import FastAPI

from punq import Container
from service_b.bootstrap.di import init_container
from service_b.infrastructure.database.utils import start_entity_mappers
from service_b.infrastructure.message_broker.base import BaseMessageBroker
from service_b.infrastructure.message_broker.init import configure_message_broker


@asynccontextmanager
async def lifespan(app: FastAPI):
    container: Container = init_container()

    start_entity_mappers()

    message_broker: BaseMessageBroker = container.resolve(BaseMessageBroker)
    await message_broker.connect()
    await configure_message_broker(message_broker)

    yield
