from functools import (
    lru_cache,
    partial,
)

from pika import BlockingConnection
from pika.adapters.blocking_connection import BlockingChannel
from punq import (
    Container,
    Scope,
)
from service_a.infrastructure.database.config import DBConfig
from service_a.infrastructure.database.init import init_database
from service_a.infrastructure.logger.base import ILogger
from service_a.infrastructure.logger.factory import create_logger_dependency
from service_a.infrastructure.message_broker.base import BaseMessageBroker
from service_a.infrastructure.message_broker.config import MessageBrokerConfig
from service_a.infrastructure.message_broker.message_broker_factory import ConnectionFactory
from service_a.infrastructure.message_broker.producer.base import BaseProducer
from service_a.infrastructure.message_broker.producer.device_task import DeviceTaskProducer
from service_a.infrastructure.message_broker.rabbit_message_broker import RabbitMQMessageBroker
from service_a.infrastructure.repositories.base import BaseDeviceTaskRepository
from service_a.infrastructure.repositories.postgres import PostgreSQLDeviceTaskRepository
from sqlalchemy import Engine

from settings.config import (
    Settings,
    settings,
)


@lru_cache(1)
def init_container() -> Container:
    return _init_container()


# Initialize the dependency injection container
def _init_container() -> Container:
    container: Container = Container()

    # Register global settings
    container.register(
        Settings,
        instance=settings,
        scope=Scope.singleton,
    )

    # Register logger
    container.register(
        ILogger,
        factory=create_logger_dependency,
        scope=Scope.singleton,
    )

    # Register database configuration
    db_config: DBConfig = DBConfig(DB_PRIVDER="postgresql")
    container.register(
        DBConfig,
        instance=db_config,
        scope=Scope.singleton,
    )

    # Register database engine
    container.register(
        Engine,
        factory=partial(init_database, db_config=db_config),
        scope=Scope.singleton,
    )

    container.register(
        BaseDeviceTaskRepository,
        PostgreSQLDeviceTaskRepository,
        scope=Scope.singleton,
    )

    # Register Message Broker
    message_broker_config: MessageBrokerConfig = MessageBrokerConfig()
    container.register(
        MessageBrokerConfig,
        instance=message_broker_config,
        scope=Scope.singleton,
    )

    container.register(ConnectionFactory, scope=Scope.singleton)

    container.register(BlockingConnection, instance=None)
    container.register(BlockingChannel, instance=None)

    container.register(
        BaseMessageBroker,
        RabbitMQMessageBroker,
        scope=Scope.singleton,
    )

    container.register(
        BaseProducer,
        DeviceTaskProducer,
    )

    return container
