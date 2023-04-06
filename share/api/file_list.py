from rest_framework.views import APIView
from django.http import JsonResponse
from user.models import User
from share.models import FileModel

class ListOfFiles(APIView):
    
    REQURIED_PARAMs = ("username", )
    
    def get(self, request, username: None):
        if username is None:
            return JsonResponse({
                "message": "Missing parameter `username` is missing! Invalid Request"
            }, status=400)
        
        try:
            user_obj = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({
                "message": "Invalid request",
            }, status=404)
        
        list_of_files = list(FileModel.objects.filter(file_owner = user_obj.pk))
        response = []
        
        for uploaded_file in list_of_files:
            response.append({
                "original_filename": uploaded_file.original_filename,
                "file_path": uploaded_file.file.name,
                "uploaded_at": uploaded_file.uploaded_at,
            })
        
        return JsonResponse({
            "total": len(list_of_files),
            "files": response,
        }, status=200)