import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class SettingsPostgres(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    NAME: str
    USER: str
    PASSWORD: str
    HOST: str = 'postgres_etl'
    PORT: int = 5432
    OPTIONS: str = '-c search_path=content'


class SettingsElasticSearch(BaseSettings):
    HOST: str = 'elasticsearch_etl'
    PORT: int = 9200
    INDEX: str = 'movies'
    SCHEMA: str = os.path.join('config', 'es_schema.json')


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
