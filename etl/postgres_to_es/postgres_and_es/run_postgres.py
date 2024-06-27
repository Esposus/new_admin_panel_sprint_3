import logging

import psycopg2

from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from psycopg2 import OperationalError

from etl.postgres_to_es.config.settings import settings_postgres
from etl.postgres_to_es.elt.backoff import func_backoff
from etl.postgres_to_es.postgres_and_es import queries_to_postgres as query
from etl.postgres_to_es.postgres_and_es import models


class PostgresConnect:

    def __init__(self):
        self.dsl: dict = {
            'dbname': settings_postgres.NAME,
            'user': settings_postgres.USER,
            'password': settings_postgres.PASSWORD,
            'host': settings_postgres.HOST,
            'port': settings_postgres.PORT,
            'options': settings_postgres.OPTIONS
        }
        self.connection = None

    @func_backoff(exception=OperationalError)
    def connect(self):
        if self.connection:
            return self.connection
        return self.create_new_connection()

    def create_new_connection(self) -> _connection:
        return psycopg2.connect(**self.dsl, cursor_factory=DictCursor)


class PostgresRun:

    def __init__(self):
        self.connection = self.connect()
        self.logger = logging.getLogger(__name__)

    @staticmethod
    def connect():
        with PostgresConnect().connect() as conn:
            return conn

    def execute_query(self, query, params=None) -> list:
        with self.connection.cursor() as cursor:
            self.logger.info(f'Выполнение запроса: {query}')
            cursor.execute(query, params)
            result = cursor.fetchall()
            self.logger.info(f'Результат запроса: {result}')
            return result

    def get_filmworks(self, timestamp) -> list:
        if filmworks := self.execute_query(query.query_filmworks(timestamp)):
            return [models.FilmworksModel(**filmwork) for filmwork in filmworks]
        return []

    def get_persons(self, timestamp) -> list:
        if persons := self.execute_query(query.query_persons(timestamp)):
            return [models.PersonsModel(**person) for person in persons]
        return []

    def get_genres(self, timestamp) -> list:
        if genres := self.execute_query(query.query_genres(timestamp)):
            return [models.GenresModel(**genre) for genre in genres]
        return []

    def get_filmwork_persons(self, persons: list) -> list:
        if filmworks := self.execute_query(query.query_filmworks_persons(persons)):
            return [models.FilmworksPersonsModel(**filmwork).id for filmwork in filmworks]
        return []

    def get_filmwork_genres(self, genres: list) -> list:
        if filmworks := self.execute_query(query.query_filmworks_genres(genres)):
            return [models.FilmworksGenresModel(**filmwork).id for filmwork in filmworks]
        return []

    def get_filmwork_all(self, filmwork_ids: tuple) -> list | None:
        if filmwork_ids:
            return self.execute_query(query.query_filmworks_all(filmwork_ids))
        return None
