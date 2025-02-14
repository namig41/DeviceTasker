from contextlib import asynccontextmanager

from fastapi import FastAPI

from punq import Container
from service_a.bootstrap.di import init_container
from service_a.infrastructure.database.utils import start_entity_mappers
from service_a.infrastructure.message_broker.base import BaseMessageBroker
from service_a.infrastructure.message_broker.init import configure_message_broker


@asynccontextmanager
async def lifespan(app: FastAPI):
    container: Container = init_container()

    start_entity_mappers()

    message_broker: BaseMessageBroker = container.resolve(BaseMessageBroker)
    message_broker.connect()
    configure_message_broker(message_broker)

    yield
