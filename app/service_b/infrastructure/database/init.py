from service_b.infrastructure.database.config import DBConfig
from service_b.infrastructure.exceptions.database import DatabaseRunFailedException
from sqlalchemy import NullPool
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase


def init_database(db_config: DBConfig) -> AsyncEngine:
    engine: AsyncEngine = create_async_engine(
        db_config.database_url,
        poolclass=NullPool,
    )
    try:
        engine.connect()
    except SQLAlchemyError:
        raise DatabaseRunFailedException()
    return engine


class Base(DeclarativeBase):
    pass
