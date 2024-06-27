import logging

from etl.postgres_to_es.postgres_and_es.run_es import ElasticSearchRun
from etl.postgres_to_es.postgres_and_es import models
from etl.postgres_to_es.postgres_and_es.run_postgres import PostgresRun
from etl.postgres_to_es.config.settings import settings_etl


class ETL:

    def __init__(self, state=None) -> None:
        self.state = state
        self.state_modified = self.state.get_state('modified')
        self.postgres = PostgresRun()
        self.elasticsearch = ElasticSearchRun()

    def extract(self) -> list:
        filmwork_ids: list = []
        person_filmwork_ids: list = []
        genre_filmwork_ids: list = []
        modified_filmwork: str = self.state_modified.get('filmwork')
        modified_person: str = self.state_modified.get('person')
        modified_genre: str = self.state_modified.get('genre')

        if filmworks := self.postgres.get_filmworks(modified_filmwork):
            self.state_modified['filmwork'] = f'{filmworks[-1].modified}'
            filmwork_ids = [filmwork.id for filmwork in filmworks]

        if persons := self.postgres.get_persons(modified_person):
            self.state_modified['person'] = f'{persons[-1].modified}'
            person_filmwork_ids = self.postgres.get_filmwork_persons(persons=[person.id for person in persons])

        if genres := self.postgres.get_genres(modified_genre):
            self.state_modified['genre'] = f'{genres[-1].modified}'
            genre_filmwork_ids = self.postgres.get_filmwork_genres(genres=[genre.id for genre in genres])

        unique_filmwork_ids = set(filmwork_ids + person_filmwork_ids + genre_filmwork_ids)

        return self.postgres.get_filmwork_all(filmwork_ids=tuple(unique_filmwork_ids))

    def prepare_for_elasticsearch(self, source_data) -> list:
        if source_data is not None:
            prepared_data: list = []
            filmwork_ids: set = {filmwork.get('fw_id') for filmwork in source_data}
        
            for filmwork_id in filmwork_ids:
                genres: list = []
                directors: list = []
                actors_names: list = []
                writers_names: list = []
                actors: list = []
                writers: list = []
                for filmwork in source_data:
                    if filmwork.get('fw_id') == filmwork_id:
                        title = filmwork.get('title')
                        imdb_rating = 0
                        description = ''
                        if type(filmwork.get('rating')) is float:
                            imdb_rating = filmwork.get('rating')
                        if type(filmwork.get('description')) is str:
                            description = filmwork.get('description')
                        if filmwork.get('genre') not in genres:
                            genres.append(filmwork.get('genre'))
                        person_name = filmwork.get('full_name')
                        person_instance = {'id': filmwork.get('person_id'), 'name': person_name}
                        if filmwork.get('role') == 'director':
                            if person_name not in directors:
                                directors.append(person_name)
                        elif filmwork.get('role') == 'actor':
                            if person_name not in actors_names:
                                actors_names.append(person_name)
                            if person_instance not in actors:
                                actors.append(person_instance)
                        elif filmwork.get('role') == 'writer':
                            if person_name not in writers_names:
                                writers_names.append(person_name)
                            if person_instance not in writers:
                                writers.append(person_instance)
                        new_filmwork = {
                            'id': filmwork_id,
                            'imdb_rating': imdb_rating,
                            'title': title,
                            'description': description,
                            'genre': genres,
                            'director': directors,
                            'actors_names': actors_names,
                            'writers_names': writers_names,
                            'actors': actors,
                            'writers': writers,
                        }
                prepared_data.append(new_filmwork)
            for filmwork in prepared_data:
                yield models.FilmworkESModel(**filmwork).model_dump()

    def load(self, film_data) -> None:
        actions: list = list()
        for film in film_data:
            actions.append(film)
            if len(actions) == settings_etl.LIMIT:
                self.elasticsearch.add_data(actions)
                actions.clear()
        else:
            if actions:
                self.elasticsearch.add_data(actions)

    def save_state(self) -> None:
        self.state.set_state('modified', self.state_modified)
