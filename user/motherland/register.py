from rest_framework.views import APIView
from django.http import JsonResponse
from uuid import uuid4
from user.serializer import UserSerializer
from datetime import datetime, timedelta
from django.contrib.sessions.backends.db import SessionStore

class RegisterAPI(APIView):

    REQUIRED_PARAM = [
        "email",
        "password"
    ]

    def post(self, request):
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
            # give 12 hours of session time for username
            expires = datetime.now() + timedelta(hours=12)
            response.set_cookie('username', new_user.username,
                                domain='',
                                path='/',
                                expires=expires,
                                secure=True,
                                samesite='None')
            
            session_store = SessionStore()
            session_store["username"] = new_user.username
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
                "message": "user registration failed! Error: {}".format(serializer.errors)
            }, status=400)
