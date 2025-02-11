from pydantic.dataclasses import dataclass


@dataclass
class DeviceTaskRequestSchema:
    timeoutInSeconds: int
    parameters: dict


@dataclass
class ProvisionResponseSchema:
    code: int
    message: str
