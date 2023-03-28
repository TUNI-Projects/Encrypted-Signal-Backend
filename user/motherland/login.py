from rest_framework.views import APIView
from django.http import JsonResponse
from user.models import User
from django.contrib.auth.hashers import check_password
from datetime import datetime

class LoginAPI(APIView):
    
    REQUIRED_PARAMS = ("email", "password")
    
    def post(self, request):
        data = request.data
        
        for field in self.REQUIRED_PARAMS:
            if field not in data:
                return JsonResponse(
                    {
                        "message": "Missing Required Parameter. {} is required".format(field)
                    }, status = 400
                )
        try:
            curr_user = User.objects.get(email=data["email"])
        except User.DoesNotExist:
            print("hello?")
            curr_user = None
        
        if curr_user is None:
            return JsonResponse({
                "message": "Email and password doesn't match!"
            }, status=404)
        else:
            print(data['password'])
            print(curr_user.password)
            if check_password(data["password"], curr_user.password):
                curr_user.last_login = datetime.utcnow()
                curr_user.save()
                
                # TODO: create some sort of cookie/token/session stuff here.
                return JsonResponse({
                    "message": "login successful!",
                    "username": curr_user.username
                }, status=202)
            else:
                return JsonResponse({
                    "message": "email and password don't match!"
                }, status=400)
        
        