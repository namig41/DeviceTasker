from dataclasses import dataclass

import pika
from pika.abc import (
    AbstractChannel,
    AbstractConnection,
)
from pika.exceptions import AMQPConnectionError

from infrastructure.exceptions.message_broker import MessageBrokerFailedConnectionException
from infrastructure.message_broker.base import BaseMessageBroker
from infrastructure.message_broker.converters import build_message
from infrastructure.message_broker.message import Message


@dataclass
class RabbitMQMessageBroker(BaseMessageBroker):
    connection: AbstractConnection
    channel: AbstractChannel

    def publish_message(
        self,
        message: Message,
        routing_key: str,
        exchange_name: str,
    ) -> None:
        rq_message = build_message(message)
        self._publish_message(rq_message, routing_key, exchange_name)

    def declare_exchange(self, exchange_name: str) -> None:
        self.channel.exchange_declare(
            exchange=exchange_name,
            exchange_type=pika.ExchangeType.topic,
            durable=True,
        )

    def _publish_message(
        self,
        rq_message: pika.BasicProperties,
        routing_key: str,
        exchange_name: str,
    ) -> None:
        self.channel.basic_publish(
            exchange=exchange_name,
            routing_key=routing_key,
            body=rq_message.body,
            properties=rq_message,
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
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host="localhost"),
            )
            self.channel = self.connection.channel()
        except AMQPConnectionError:
            raise MessageBrokerFailedConnectionException()

    def close(self) -> None:
        if self.connection and self.connection.is_open:
            self.connection.close()
