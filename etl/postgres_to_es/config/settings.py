import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class PostgresSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_OPTIONS: str


class ElasticSearchSettings(BaseSettings):
    ES_HOST: str
    ES_PORT: int
    ES_INDEX: str
    ES_SCHEMA: str


class ETLSettings(BaseSettings):
    LIMIT: int
    STATE_FILE: str
    TIME_SLEEP: int


settings_postgres = PostgresSettings()
settings_es = ElasticSearchSettings()
settings_etl = ETLSettings()
