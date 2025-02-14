from datetime import (
    datetime,
    timezone,
)
from uuid import UUID

import orjson
import pika

from infrastructure.message_broker.message import Message


def build_message(message: Message) -> pika.Message:
    return pika.Message(
        body=orjson.dumps(
            {"message_type": message.message_type, "data": message.data},
        ),
        message_id=str(message.id),
        content_type="application/json",
        delivery_mode=pika.DeliveryMode.PERSISTENT,
        headers={},
    )


def from_pika_message(aio_message: pika.Message) -> Message:
    try:
        payload = orjson.loads(aio_message.body)

        return Message(
            id=UUID(aio_message.message_id),
            data=payload.get("data", ""),
            message_type=payload.get("message_type", "message"),
            created_at=datetime.now(timezone.utc),
        )
    except (orjson.JSONDecodeError, ValueError, KeyError) as e:
        raise ValueError(f"Ошибка при декодировании сообщения: {e}") from e
