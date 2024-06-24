import logging
from functools import wraps
from time import sleep

logging.basicConfig(filename='backoff.log', level=logging.INFO, filemode='w')
log = logging.getLogger()


def func_backoff(exception, start_sleep_time=0.1, factor=2, border_sleep_time=10, max_connection=3):

    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            count_connection = 0
            sleep_time = start_sleep_time
            while True:
                try:
                    count_connection += 1
                    log.info(f'Подключение № {count_connection} из {max_connection}!')
                    return func(*args, **kwargs)
                except exception as error:
                    log.error(f'Ошибка:{error}!')

                    if count_connection == max_connection:
                        log.info('Превышение количества подключений!')
                        raise 'Превышение количества подключений.'

                    if sleep_time >= border_sleep_time:
                        sleep_time = border_sleep_time
                    else:
                        sleep_time += start_sleep_time * (factor ** 2)

                    sleep(sleep_time)

        return inner

    return func_wrapper
