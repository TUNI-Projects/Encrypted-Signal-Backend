from rest_framework.views import APIView
from django.http import JsonResponse
from uuid import uuid4
from user.serializer import UserSerializer

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
                        "message": "Missing Required Parameter. {} is required".format(item)
                    }, status = 400
                )
        
        username = str(uuid4())[:8]
        data["username"] = username
        
        serializer = UserSerializer(data = data)
        if serializer.is_valid():
            new_user = serializer.save()
            
            return JsonResponse({
                "message": "new user created successfully",
                "username": new_user.username,
                "email": new_user.email,
                "password": "has been set!"
            }, status=201)
        else:
            return JsonResponse({
                "message": "user registration failed! Error: {}".format(serializer.errors)
            }, status=400)
            
        