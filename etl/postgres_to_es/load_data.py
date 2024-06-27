import json
import logging
from time import sleep

from etl.postgres_to_es.config.settings import settings_etl
from etl.postgres_to_es.elt.run_etl import ETL
from etl.postgres_to_es.elt.state import JsonFileStorage, State


def load_data() -> None:
    storage = JsonFileStorage(settings_etl.STATE_FILE)
    etl_state = State(storage)

    while True:
        etl = ETL(state=etl_state)
        data = etl.extract()
        if data is None:
            print('No data')
        prepared_data = etl.prepare_for_elasticsearch(data)
        etl.load(prepared_data)
        etl.save_state()

        sleep(settings_etl.TIME_SLEEP)


if __name__ == '__main__':
    start_state = {"modified": {
        "filmwork": "0001-01-01 00:00:00",
        "person": "0001-01-01 00:00:00",
        "genre": "0001-01-01 00:00:00"
    }
    }
    with open('state_file.json', 'w') as file:
        json.dump(start_state, file)

    load_data()
