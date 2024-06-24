from config.settings import settings_etl


def query_filmworks(timestamp) -> str:
    return f"""
        SELECT id, modified
        FROM content.film_work
        WHERE modified > {timestamp}
        ORDER BY modified
        LIMIT {settings_etl.LIMIT}    
    """


def query_persons(timestamp) -> str:
    return f"""
        SELECT id, modified
        FROM content.person
        WHERE modified > {timestamp}
        ORDER BY modified
        LIMIT {settings_etl.LIMIT}    
    """


def query_genres(timestamp) -> str:
    return f"""
        SELECT id, modified
        FROM content.genre
        WHERE modified > {timestamp}
        ORDER BY modified
        LIMIT {settings_etl.LIMIT}    
    """
