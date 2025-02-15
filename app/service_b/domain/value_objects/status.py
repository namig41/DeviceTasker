from enum import (
    auto,
    Enum,
)


class TaskStatus(Enum):
    NOTHING = auto()
    COMPLETED = auto()
    RUNNING = auto()
