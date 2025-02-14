from dataclasses import dataclass

import pika
from pika import BlockingConnection
from pika.adapters.blocking_connection import BlockingChannel
from pika.exceptions import AMQPConnectionError
from service_a.infrastructure.message_broker.config import MessageBrokerConfig


@dataclass
class ConnectionFactory:
    config: MessageBrokerConfig

    def get_connection(self) -> BlockingConnection:
        """
        Создает и возвращает синхронное соединение с RabbitMQ.
        """
        try:
            connection = BlockingConnection(
                pika.ConnectionParameters(
                    host=self.config.host,
                    port=self.config.port,
                    credentials=pika.PlainCredentials(
                        username=self.config.login,
                        password=self.config.password,
                    ),
                ),
            )
            return connection
        except AMQPConnectionError as e:
            raise Exception(f"Failed to connect to RabbitMQ: {e}")


@dataclass
class ChannelFactory:
    connection_factory: ConnectionFactory

    def get_channel(self) -> BlockingChannel:
        """
        Создает и возвращает канал (channel) для работы с RabbitMQ.
        """
        connection = self.connection_factory.get_connection()
        return connection.channel()
