from contextlib import asynccontextmanager

from fastapi import FastAPI

from punq import Container

from bootstrap.di import init_container
from infrastructure.database.utils import start_entity_mappers
from infrastructure.message_broker.base import BaseMessageBroker
from infrastructure.message_broker.init import configure_message_broker


@asynccontextmanager
async def lifespan(app: FastAPI):
    container: Container = init_container()

    start_entity_mappers()

    message_broker: BaseMessageBroker = container.resolve(BaseMessageBroker)
    await message_broker.connect()
    await configure_message_broker(message_broker)

    yield
