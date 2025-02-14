from enum import (
    auto,
    Enum,
)


class TaskStatus(Enum):
    NOTHING = auto()
    RUNNING = auto()
    STOPPED = auto()
    COMPLETED = auto()
