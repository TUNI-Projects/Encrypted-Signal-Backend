from django.contrib.sessions.backends.db import SessionStore
from django.http import JsonResponse
from datetime import datetime, timedelta


def cookie_monster(response, key: str, val: str):
    """Adds a cookie to the response object

    Args:
        response (_type_): _description_
        key (str): _description_
        val (str): _description_

    Returns:
        _type_: _description_
    """
    expires = datetime.now() + timedelta(minutes=5)
    response.set_cookie(key, val,
                        domain='',
                        path='/',
                        expires=expires,
                        secure=True,
                        samesite='None')
    return response


def session_manager(response, username: str):
    """
    genereates a session at the backend then creates a cookie and add that cookie with the response object

    Args:
        response (Any): _description_
        username (str): _description_

    Returns:
        response: response object
    """
    session_store = SessionStore()
    session_store["username"] = username
    session_store.create()
    session_id = session_store.session_key
    response = cookie_monster(response, "sessionId", session_id)
    response['SameSite'] = 'None'
    return response
