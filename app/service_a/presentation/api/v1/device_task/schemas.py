from pydantic import PositiveInt
from pydantic.dataclasses import dataclass


@dataclass
class DeviceTaskRequestSchema:
    timeoutInSeconds: PositiveInt
    parameters: dict


@dataclass
class ProvisionResponseSchema:
    code: int
    message: str
