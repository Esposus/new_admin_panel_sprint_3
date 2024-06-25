import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class SettingsPostgres(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str = 'postgres_etl'
    DB_PORT: int = 5432
    DB_OPTIONS: str = '-c search_path=content'


class SettingsElasticSearch(BaseSettings):
    ES_HOST: str = 'elasticsearch_etl'
    ES_PORT: int = 9200
    ES_INDEX: str = 'movies'
    ES_SCHEMA: str = os.path.join('config', 'es_schema.json')


class SettingsETL(BaseSettings):
    LIMIT: int = 100
    STATE_FILE: str = 'state_file.json'
    TIME_SLEEP: int = 5

    FILM_WORK_TABLE = 'content.film_work'
    PERSON_TABLE = 'content.person'
    GENRE_TABLE = 'content.genre'
    PERSON_FILM_WORK_TABLE = 'content.person_film_work'
    GENRE_FILM_WORK_TABLE = 'content.genre_film_work'


settings_postgres = SettingsPostgres()
settings_es = SettingsElasticSearch()
settings_etl = SettingsETL()
