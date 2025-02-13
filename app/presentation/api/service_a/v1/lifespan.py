from contextlib import asynccontextmanager

from fastapi import FastAPI

from punq import Container

from bootstrap.di import init_container
from infrastructure.message_broker.base import BaseMessageBroker


@asynccontextmanager
async def lifespan(app: FastAPI):
    container: Container = init_container()  # noqa

    message_broker: BaseMessageBroker = container.resolve(BaseMessageBroker)
    await message_broker.connect()

    yield
