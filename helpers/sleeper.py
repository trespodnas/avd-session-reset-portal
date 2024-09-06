from time import sleep
from functools import wraps


def add_sleep_time(seconds):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            sleep(seconds)
            return func(*args, **kwargs)
        return wrapper
    return decorator