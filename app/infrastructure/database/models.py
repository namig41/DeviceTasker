from sqlalchemy import (
    Column,
    Integer,
    JSON,
    String,
    Table,
    text,
    TIMESTAMP,
)
from sqlalchemy.orm import registry


mapper_registry = registry()
metadata = mapper_registry.metadata


tasks = Table(
    "tasks",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("task_id", String(50), nullable=False, unique=True),
    Column("equipment_id", String(50), nullable=False),
    Column("parameters", JSON, nullable=True),
    Column("status", String(50), default="Running"),
    Column("created_at", TIMESTAMP(timezone=True), server_default=text("NOW()")),
)
