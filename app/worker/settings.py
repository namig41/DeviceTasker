from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    SERVICE_A_API_HOST: str
    SERVICE_A_API_PORT: int

    @property
    def get_service_url(self) -> str:
        return f"http://{self.SERVICE_A_API_HOST}:{self.SERVICE_A_API_PORT}"

    MESSAGE_BROKER_HOST: str
    MESSAGE_BROKER_PORT: int
    MESSAGE_BROKER_USER: str
    MESSAGE_BROKER_PASSWORD: str

    @property
    def get_message_broker_url(self) -> str:
        return f"""amqp://{self.MESSAGE_BROKER_USER}:{self.MESSAGE_BROKER_PASSWORD}
    @{self.MESSAGE_BROKER_HOST}:{self.MESSAGE_BROKER_PORT}/"""


settings = Settings()
