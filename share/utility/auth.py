from rest_framework import authentication
from rest_framework import exceptions
from django.contrib.sessions.backends.db import SessionStore
from user.models import User


def auth_required(view_func):
    def wrapper(request, *args, **kwargs):
        # Check if the user is authenticated
        session_id = None
        if 'Cookie' in request.headers:
            cookies = request.headers['Cookie']
            for cookie in cookies.split(';'):
                if 'sessionId' in cookie:
                    session_id = cookie.split('=')[1]
                    break
            session_obj = SessionStore(session_key=session_id)
            print(session_obj)
            try:
                user = User.objects.get(username=session_obj["username"])        
                request.user = user
                print(request.user)
            except User.DoesNotExist:
                raise exceptions.AuthenticationFailed('Authentication required!')
        else:
            exceptions.AuthenticationFailed('Authentication required!')

        # Call the view function if authenticated
        return view_func(request, *args, **kwargs)

    return wrapper
