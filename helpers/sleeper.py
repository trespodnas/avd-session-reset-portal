from time import sleep
from functools import wraps

from helpers.session_reset import end_user_session

DEFAULT_SLEEP_TIME = 9

def add_sleep_time(seconds):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            sleep(seconds)
            return func(*args, **kwargs)
        return wrapper
    return decorator


def end_user_session_delayed(user_upn, sleep_time=DEFAULT_SLEEP_TIME):
    return sleep(sleep_time), end_user_session(user_upn)


if __name__ == '__main__':
    exit(0)