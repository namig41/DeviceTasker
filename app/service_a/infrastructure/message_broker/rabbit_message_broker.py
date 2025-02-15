from dataclasses import dataclass

import pika
import pika.exchange_type
from pika.adapters.blocking_connection import BlockingChannel
from pika.exceptions import AMQPConnectionError
from service_a.infrastructure.exceptions.message_broker import MessageBrokerFailedConnectionException
from service_a.infrastructure.message_broker.base import BaseMessageBroker
from service_a.infrastructure.message_broker.converters import build_message
from service_a.infrastructure.message_broker.message import Message
from service_a.infrastructure.message_broker.message_broker_factory import ConnectionFactory


@dataclass
class RabbitMQMessageBroker(BaseMessageBroker):
    connection_factory: ConnectionFactory
    channel: BlockingChannel

    def publish_message(
        self,
        message: Message,
        routing_key: str,
        exchange_name: str,
    ) -> None:
        properties, body = build_message(message)
        self._publish_message(properties, body, routing_key, exchange_name)

    def declare_exchange(self, exchange_name: str) -> None:
        self.channel.exchange_declare(
            exchange=exchange_name,
            exchange_type="direct",
            durable=True,
        )

    def _publish_message(
        self,
        properties: pika.BasicProperties,
        body: bytes,
        routing_key: str,
        exchange_name: str,
    ) -> None:
        self.channel.basic_publish(
            exchange=exchange_name,
            routing_key=routing_key,
            body=body,
            properties=properties,
        )

    def declare_queue(
        self,
        queue_name: str,
        exchange_name: str,
        routing_key: str,
    ) -> None:
        self.channel.queue_declare(
            queue=queue_name,
            durable=True,
        )
        self.channel.queue_bind(
            queue=queue_name,
            exchange=exchange_name,
            routing_key=routing_key,
        )

    def connect(self) -> None:
        try:
            self.connection = self.connection_factory.get_connection()
            self.channel = self.connection.channel()
        except AMQPConnectionError:
            raise MessageBrokerFailedConnectionException()

    def close(self) -> None:
        if self.connection and self.connection.is_open:
            self.connection.close()
