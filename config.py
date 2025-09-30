from pydantic_settings import BaseSettings, SettingsConfigDict


# TODO: Create the settings class to read environment variables


class Settings(BaseSettings):
    X_API_KEY: str

    model_config = SettingsConfigDict(env_file=".env",env_file_encoding="utf-8")




settings = Settings()