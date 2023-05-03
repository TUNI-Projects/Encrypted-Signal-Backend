from datetime import datetime

from django.contrib.auth.hashers import check_password
from django.contrib.sessions.backends.db import SessionStore
from django.http import JsonResponse
from rest_framework.views import APIView
from share.utility.cookie import cookie_monster
from es_backend.settings import DEBUG
from user.models import User


class LoginAPI(APIView):

    REQUIRED_PARAMS = ("email", "password")

    def post(self, request):
        data = request.data
        IS_DEBUG = DEBUG
        for field in self.REQUIRED_PARAMS:
            if field not in data:
                return JsonResponse(
                    {
                        "status": 400,
                        "message": "Missing Required Parameter. {} is required".format(field)
                    }, status=400
                )
        try:
            curr_user = User.objects.get(email=data["email"])
        except User.DoesNotExist:
            curr_user = None

        if curr_user is None:
            return JsonResponse({
                "status": 404,
                "message": "Email and password doesn't match!"
            }, status=404)
        else:
            if check_password(data["password"], curr_user.password):
                curr_user.last_login = datetime.utcnow()
                curr_user.save()

                response = JsonResponse({
                    "status": 202,
                    "message": "login successful!",
                    "username": curr_user.username
                }, status=202)

                session_store = SessionStore()
                session_store["username"] = curr_user.username
                session_store.create()
                session_id = session_store.session_key

                response = cookie_monster(
                    response, "username", curr_user.username)
                response = cookie_monster(response, "sessionId", session_id)
                if IS_DEBUG:
                    response['SameSite'] = 'Strict'
                else:
                    response['SameSite'] = 'None'
                return response
            else:
                return JsonResponse({
                    "status": 400,
                    "message": "email and password don't match!"
                }, status=400)
