from rest_framework.views import APIView
from django.http import JsonResponse
from user.models import User
from share.models import FileModel
from datetime import datetime, timedelta


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

        list_of_files = list(FileModel.objects.filter(file_owner=user_obj.pk))
        response = []

        for uploaded_file in list_of_files:
            response.append({
                "file_id": uploaded_file.index,
                "original_filename": uploaded_file.original_filename,
                "file_path": None,
                "uploaded_at": uploaded_file.uploaded_at,
                "file_type": uploaded_file.file_type,
            })

        response = JsonResponse({
            "total": len(list_of_files),
            "files": response,
        })
        return response
