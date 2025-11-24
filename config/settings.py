from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # database
    postgres_url: str

    # fast-api

    ## authentication
    secret_key: str
    jwt_algorithm: str
    access_token_expire_minutes: int = 15

    ## registration
    invitation_code: str

    # image detection model
    detection_upload_url: str
    detection_model_path: str

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
