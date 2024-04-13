from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    SECRET_AUTH: str
    COOKIES: str
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()