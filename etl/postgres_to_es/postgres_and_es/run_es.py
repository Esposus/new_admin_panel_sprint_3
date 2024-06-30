import json

from elasticsearch import Elasticsearch, helpers

from etl.postgres_to_es.config.settings import settings_es
from etl.postgres_to_es.elt.backoff import func_backoff as backoff


class ElasticSearchRun:

    def __init__(self):
        self.connection = Elasticsearch([
            {
                'host': settings_es.HOST,
                'port': settings_es.PORT,
                'scheme': 'http',
            }
        ])
        self.index_name = settings_es.INDEX
        self.schema = self.get_schema(settings_es.SCHEMA)
        self.indices = self.get_indices()

    @staticmethod
    def get_schema(file_path: str) -> str:
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f'File {file_path} not found')

    @backoff(exception=ConnectionError)
    def get_indices(self) -> list:
        indices = list(self.connection.indices.get_alias())
        if self.index_name not in indices:
            self.create_index(self.index_name)
        return indices

    def create_index(self, index_name: str) -> None:
        if body := self.schema:
            self.connection.indices.create(index=index_name, body=body)

    @backoff(exception=ConnectionError)
    def get_connection(self):
        if self.connection.ping():
            return True
        raise ConnectionError

    @backoff(exception=ConnectionError)
    def add_data(self, actions) -> None:
        helpers.bulk(
            client=self.connection,
            actions=[
                {'_index': self.index_name, '_id': action.get('id'), **action} for action in actions
            ]
        )
