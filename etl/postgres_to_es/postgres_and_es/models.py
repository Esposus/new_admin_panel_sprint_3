from datetime import datetime

from pydantic import BaseModel


class UUIDMixin(BaseModel):
    id: str


class ModifiedMixin(BaseModel):
    modified: datetime


class FilmworksModel(UUIDMixin, ModifiedMixin):
    """Модель фильмов"""


class PersonsModel(UUIDMixin, ModifiedMixin):
    """Модель людей"""


class GenresModel(UUIDMixin, ModifiedMixin):
    """Модель жанров"""


class FilmworksPersonsModel(UUIDMixin, ModifiedMixin):
    """Модель связи фильмов и людей"""


class FilmworksGenresModel(UUIDMixin, ModifiedMixin):
    """Модель связи фильмов и жанров"""


class PersonESModel(BaseModel):
    """Модель для ES для людей"""
    name: str


class FilmworkESModel(BaseModel):
    """Модель для ES для фильмов"""
    imdb_rating: float = None
    genre: list[str] = None
    title: str
    description: str = None
    director: list[str] = None
    actors_names: list[str] = None
    writers_names: list[str] = None
    actors: list[PersonESModel] = None
    writers: list[PersonESModel] = None
