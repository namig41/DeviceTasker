from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True, kw_only=True)
class Message:
    id: UUID
    data: dict
    message_type: str
    created_at: datetime
