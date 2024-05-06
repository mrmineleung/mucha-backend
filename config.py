from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    HOST: str
    PORT: int
    SECRET_KEY: str
    MONGO_URI: str
    MONGO_MUSIC_CHARTS_DBNAME: str
    BASE_URL: str
    MEDIA_BASE_URL: str
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME: str
    GOOGLE_OAUTH_REDIRECT_URL: str
    GOOGLE_OAUTH_CLIENT_ID: str
    GOOGLE_OAUTH_CLIENT_SECRET: str


    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
