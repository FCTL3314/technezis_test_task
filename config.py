from decouple import config
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    token: str = config("TOKEN", cast=str)
    db_engine: str = config("DB_ENGINE", cast=str)
