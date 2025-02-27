import logging
from dataclasses import dataclass

from service_b.infrastructure.logger.base import ILogger


@dataclass
class Logger(ILogger):

    logger: logging.Logger
    error_logger: logging.Logger

    def info(self, message: str) -> None:
        self.logger.info(message)

    def error(self, message: str) -> None:
        self.error_logger.error(message)

    def debug(self, message: str) -> None:
        self.logger.debug(message)
