from dataclasses import (
    dataclass,
    field,
)
from datetime import datetime
from uuid import UUID

from service_b.tools.time_utils import ts_now
from uuid6 import uuid7


@dataclass(frozen=True, kw_only=True)
class Message:
    id: UUID = field(default_factory=uuid7)
    data: dict = field(default_factory=dict)
    message_type: str = "message"
    created_at: datetime = field(default_factory=ts_now)
