from rest_framework.views import APIView
from django.http import JsonResponse
from uuid import uuid4
from user.serializer import UserSerializer
from share.utility.cookie import cookie_monster
from django.contrib.sessions.backends.db import SessionStore
from es_backend.settings import DEBUG


class RegisterAPI(APIView):

    REQUIRED_PARAM = [
        "email",
        "password"
    ]

    def post(self, request):
        IS_DEBUG = DEBUG
        
        data = request.data
        for item in self.REQUIRED_PARAM:
            if item not in data:
                return JsonResponse(
                    {
                        "status": 400,
                        "message": "Missing Required Parameter. {} is required".format(item)
                    }, status=400
                )

        username = str(uuid4())[:8]
        data["username"] = username

        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            new_user = serializer.save()

            response = JsonResponse({
                "status": 201,
                "message": "new user created successfully",
                "username": new_user.username,
                "email": new_user.email,
                "password": "has been set!"
            }, status=201)

            session_store = SessionStore()
            session_store["username"] = new_user.username
            session_store.create()
            session_id = session_store.session_key

            response = cookie_monster(
                response, "username", new_user.username)
            response = cookie_monster(response, "sessionId", session_id)
            if IS_DEBUG:
                response['SameSite'] = 'Strict'
            else:
                response['SameSite'] = 'None'
            return response
        else:
            return JsonResponse({
                "status": 400,
                "message": "user registration failed! Error: {}".format(serializer.errors)
            }, status=400)
