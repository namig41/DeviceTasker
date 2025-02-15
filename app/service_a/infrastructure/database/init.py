from service_a.infrastructure.database.config import DBConfig
from service_a.infrastructure.exceptions.database import DatabaseRunFailedException
from sqlalchemy import (
    create_engine,
    Engine,
)
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import DeclarativeBase


def init_database(db_config: DBConfig) -> Engine:
    """
    Инициализирует синхронное подключение к базе данных и возвращает объект Engine.
    """
    engine: Engine = create_engine(
        db_config.database_url,
    )
    try:
        ...
    except SQLAlchemyError as e:
        raise DatabaseRunFailedException(f"Failed to connect to the database: {e}")
    return engine


class Base(DeclarativeBase):
    """
    Базовый класс для всех моделей SQLAlchemy.
    """
