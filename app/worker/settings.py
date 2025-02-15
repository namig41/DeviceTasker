from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    SERVICE_B_API_HOST: str
    SERVICE_B_API_PORT: int

    @property
    def get_service_url(self) -> str:
        return f"https://{self.SERVICE_B_API_HOST}"

    MESSAGE_BROKER_HOST: str
    MESSAGE_BROKER_PORT: int
    MESSAGE_BROKER_USER: str
    MESSAGE_BROKER_PASSWORD: str

    @property
    def get_message_broker_url(self) -> str:
        return (
            f"amqp://{self.MESSAGE_BROKER_USER}:{self.MESSAGE_BROKER_PASSWORD}"
            f"@{self.MESSAGE_BROKER_HOST}:{self.MESSAGE_BROKER_PORT}/"
        )


settings = Settings()
