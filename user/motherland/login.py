import bleach
from datetime import datetime

from django.contrib.auth.hashers import check_password
from django.contrib.sessions.backends.db import SessionStore
from django.http import JsonResponse
from rest_framework.views import APIView
from share.utility.cookie import session_manager
from user.models import User


class LoginAPI(APIView):

    REQUIRED_PARAMS = ("email", "password")

    def post(self, request):
        data = request.data
        for field in self.REQUIRED_PARAMS:
            if field not in data:
                return JsonResponse(
                    {
                        "status": 400,
                        "message": "Missing Required Parameter. {} is required".format(field)
                    }, status=400
                )

        sanitized_email = bleach.clean(data["email"], strip=True)
        try:
            curr_user = User.objects.get(email=sanitized_email)
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

                response = session_manager(response, curr_user.username)
                return response
            else:
                return JsonResponse({
                    "status": 400,
                    "message": "email and password don't match!"
                }, status=400)
