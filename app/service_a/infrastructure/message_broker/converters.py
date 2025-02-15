from uuid import UUID

import orjson
import pika
from service_a.infrastructure.message_broker.message import Message
from service_a.tools.time_utils import ts_now


def build_message(message: Message) -> tuple[pika.BasicProperties, bytes]:
    return pika.BasicProperties(
        message_id=str(message.id),
        content_type="application/json",
        delivery_mode=2,
        headers={},
    ), orjson.dumps(
        {
            "message_type": message.message_type,
            "data": message.data,
        },
    )


def from_pika_message(aio_message: pika.spec.BasicProperties, body: bytes) -> Message:
    try:
        payload = orjson.loads(body)
        return Message(
            id=UUID(aio_message.message_id),
            data=payload.get("data", ""),
            message_type=payload.get("message_type", "message"),
            created_at=ts_now(),
        )
    except (orjson.JSONDecodeError, ValueError, KeyError) as e:
        raise ValueError(f"Ошибка при декодировании сообщения: {e}") from e
