from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PYTHONPATH: str

    SERVICE_A_API_HOST: str
    SERVICE_A_API_PORT: int
    SERVICE_A_API_CORS: list[str]

    SERVICE_B_API_HOST: str
    SERVICE_B_API_PORT: int
    SERVICE_B_API_CORS: list[str]

    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_PROVIDER: str

    PGADMIN_EMAIL: str
    PGADMIN_PASSWORD: str

    MESSAGE_BROKER_HOST: str
    MESSAGE_BROKER_PORT: int
    MESSAGE_BROKER_UI_PORT: int
    MESSAGE_BROKER_USER: str
    MESSAGE_BROKER_PASSWORD: str


settings: Settings = Settings()
