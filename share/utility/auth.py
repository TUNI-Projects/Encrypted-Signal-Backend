from django.contrib.sessions.backends.db import SessionStore
from django.http import JsonResponse
from user.models import User
import functools


def protected(function):
    @functools.wraps(function)
    def wrapper(self, request, *args, **kwargs):
        cookies = request.headers.get("Cookie")
        if cookies is None:
            return JsonResponse({
                "message": "Authentication Failure!"
            }, status=401)

        for cookie in cookies.split(';'):
            if 'sessionId' in cookie:
                session_id = cookie.split('=')[1]
                break

        if session_id is None:
            return JsonResponse({
                "message": "Authentication Failure!"
            }, status=401)

        try:
            session_obj = SessionStore(session_key=session_id)
            username = session_obj["username"]
        except KeyError:
            return JsonResponse({
                "message": "Authentication Failure!"
            }, status=401)

        try:
            user_obj = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({
                "message": "Authentication Failure!",
            }, status=404)

        request.user = user_obj
        return function(self, request, *args, **kwargs)
    return wrapper


def deprecated(function):
    """deprecated decorator

    Args:
        function (_type_): _description_

    Returns:
        _type_: _description_
    """
    @functools.wraps(function)
    def wrapper(self, request, *args, **kwargs):
        return JsonResponse({
            "message": "This API/Function has been deprecated!"
        }, status=410)
    return wrapper
