from config.settings import settings_etl


FILM_WORK_TABLE = settings_etl.FILM_WORK_TABLE
PERSON_TABLE = settings_etl.PERSON_TABLE
GENRE_TABLE = settings_etl.GENRE_TABLE
PERSON_FILM_WORK_TABLE = settings_etl.PERSON_FILM_WORK_TABLE
GENRE_FILM_WORK_TABLE = settings_etl.GENRE_FILM_WORK_TABLE
LIMIT = settings_etl.LIMIT


def query_filmworks(timestamp) -> str:
    """Запрос на получение обновлённых фильмов за заданный промежуток времени."""
    return f"""
        SELECT id, modified
        FROM {FILM_WORK_TABLE}
        WHERE modified > '{timestamp}'
        ORDER BY modified
        LIMIT {LIMIT};
    """


def query_persons(timestamp) -> str:
    """Запрос на получение обновлённых людей за заданный промежуток времени."""
    return f"""
        SELECT id, modified
        FROM {PERSON_TABLE}
        WHERE modified > '{timestamp}'
        ORDER BY modified
        LIMIT {LIMIT};
    """


def query_genres(timestamp) -> str:
    """Запрос на получение обновлённых жанров за заданный промежуток времени."""
    return f"""
        SELECT id, modified
        FROM {GENRE_TABLE}
        WHERE modified > '{timestamp}'
        ORDER BY modified
        LIMIT {LIMIT};
    """


def query_filmworks_persons(persons: list) -> str:
    """Запрос на получение фильмов с обновленными людьми."""
    return f"""
        SELECT fw.id, fw.modified
        FROM {FILM_WORK_TABLE} fw
        LEFT JOIN {PERSON_FILM_WORK_TABLE} pfw ON pfw.film_work_id=fw.id
        WHERE pfw.person_id {f"IN {tuple(persons)}" if len(persons) > 1 else f"='{persons[0]}'"}
        ORDER BY fw.modified
        LIMIT {LIMIT};
    """


def query_filmworks_genres(genres: list) -> str:
    """Запрос на получение фильмов с обновленными жанрами."""
    return f"""
        SELECT fw.id, fw.modified
        FROM {FILM_WORK_TABLE} fw
        LEFT JOIN {GENRE_FILM_WORK_TABLE} gfw ON gfw.film_work_id=fw.id
        WHERE gfw.genre_id {f"IN {tuple(genres)}" if len(genres) > 1 else f"='{genres[0]}'"}
        ORDER BY fw.modified
        LIMIT {LIMIT};
    """


def query_filmworks_all(filmwork_ids: tuple) -> str:
    """Запрос на получение всей недостающей информации о фильмах."""
    return f"""
        SELECT
        fw.id as fw_id, 
        fw.title, 
        fw.description, 
        fw.rating, 
        fw.type, 
        fw.created, 
        fw.modified, 
        pfw.role, 
        p.id as person_id, 
        p.full_name,
        g.name as genre
        FROM {FILM_WORK_TABLE} fw
        LEFT JOIN {PERSON_FILM_WORK_TABLE} pfw ON pfw.film_work_id=fw.id
        LEFT JOIN {PERSON_TABLE} p ON p.id=pfw.person_id
        LEFT JOIN {GENRE_FILM_WORK_TABLE} gfw ON gfw.film_work_id=fw.id
        LEFT JOIN {GENRE_TABLE} g ON g.id=gfw.genre_id
        WHERE fw.id {f"IN {tuple(filmwork_ids)}" if len(filmwork_ids) > 1 else f"='{filmwork_ids[0]}'"};
    """
