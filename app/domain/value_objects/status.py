from enum import Enum


class TaskStatus(Enum):
    NOTHING = "NOTHING"
    RUNNING = "RUNNING"
    STOPPED = "STOPPED"
    COMPLETED = "COMPLETED"
