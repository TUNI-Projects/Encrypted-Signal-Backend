from rest_framework.views import APIView
from django.http import JsonResponse
from user.models import User
from django.contrib.auth.hashers import check_password
from datetime import datetime, timedelta
from django.contrib.sessions.backends.db import SessionStore


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

                # TODO: create some sort of cookie/token/session stuff here.
                response = JsonResponse({
                    "status": 202,
                    "message": "login successful!",
                    "username": curr_user.username
                }, status=202)

                # give 12 hours of session time for username
                expires = datetime.now() + timedelta(hours=12)
                response.set_cookie('username', curr_user.username,
                                    domain='',
                                    path='/',
                                    expires=expires,
                                    secure=True,
                                    samesite='None')
                
                session_store = SessionStore()
                session_store["username"] = curr_user.username
                session_store.create()
                session_id = session_store.session_key
                response.set_cookie(
                    key="sessionId",
                    value=session_id,
                    expires=expires,
                    domain='',
                    path='/',
                    secure=True,
                    samesite='None'
                )
                response['SameSite'] = 'None'
                return response
            else:
                return JsonResponse({
                    "status": 400,
                    "message": "email and password don't match!"
                }, status=400)
