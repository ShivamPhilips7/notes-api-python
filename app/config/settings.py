from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # Kafka
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"
    KAFKA_TOPIC: str = "notes.events"
    KAFKA_CLIENT_ID: str = "notes-api"

    model_config = SettingsConfigDict(
        env_file=".env.local",
        extra="ignore"
    )


settings = Settings()