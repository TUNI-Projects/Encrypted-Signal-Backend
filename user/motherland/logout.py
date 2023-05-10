from django.contrib.sessions.backends.db import SessionStore
from django.http import JsonResponse
from rest_framework.views import APIView
from user.models import User
from share.utility.auth import protected


class LogoutAPI(APIView):

    @protected
    def post(self, request):
        cookies = request.headers.get("Cookie")
        for cookie in cookies.split(';'):
            if 'sessionId' in cookie:
                session_id = cookie.split('=')[1]
                break

        try:
            session_obj = SessionStore(session_key=session_id)
            session_obj.delete()

            return JsonResponse({
                "message": "You are logged out!",
            }, status=200)
        except KeyError:
            return JsonResponse({
                "message": "Authentication Failure!"
            }, status=401)
