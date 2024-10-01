import random
import string


session_data = {'session_state': {}}


def unique_token(length=10):
    return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(length))


def add_to_user_state(upn):
    session_data['session_state'][upn] = {
        'upn': upn,
        'my_key': unique_token()
    }


def get_user_upn_from_state(email):
    user_data = session_data['session_state'].get(email)
    if user_data:
        return user_data['upn']
    else:
        return None


def get_user_token_from_state(email):
    user_data = session_data['session_state'].get(email)
    if user_data:
        return user_data['my_key']
    else:
        return None


def remove_user_from_state(upn):
    del session_data['session_state'][upn]


def show_all_user_states():
    return session_data['session_state'].keys()


if __name__ == '__main__':
    exit(0)