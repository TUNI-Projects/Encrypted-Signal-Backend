import bleach
from rest_framework.views import APIView
from django.http import JsonResponse
from uuid import uuid4
from user.serializer import UserSerializer
from share.utility import check_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


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
        data['email'] = bleach.clean(data["email"], strip=True)
        if not check_password(data['password']):
            return JsonResponse({
                "message": "Your password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one digit, and one special character.",
            }, status=400)

        try:
            # Check if the password is a common password
            validate_password(data['password'])
        except ValidationError as e:
            return JsonResponse(
                {
                    "status": 400,
                    "message": "Invalid password. {}".format(e),
                }, status=400
            )

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
            return response
        else:
            return JsonResponse({
                "status": 400,
                "message": "user registration failed! Error: {}".format(serializer.errors)
            }, status=400)
