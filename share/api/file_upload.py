from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import JsonResponse
from share.serializer import UploadSerializer
from user.models import User

class FileUploadAPI(APIView):
    
    parser_classes = (MultiPartParser, FormParser)
    REQUIRED_PARAMETERS = ("file", "username")
    
    def post(self, request):
        data = request.data
        original_filename = data['file']
        username = data["username"]
        
        try:
            owner_obj = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({
                "message": "Invalid Request"
            }, status=403)
        
        data["original_filename"] = original_filename.name
        data["file_owner"] = owner_obj.pk
        
        upload_serializer = UploadSerializer(data = data)
        if upload_serializer.is_valid():
            upload_serializer.save()
            return JsonResponse({
                "data": upload_serializer.data
            }, status=201)
        else:
            return JsonResponse({
                "message": upload_serializer.errors,
            }, status=400)