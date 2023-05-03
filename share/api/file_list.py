from django.http import JsonResponse
from rest_framework.views import APIView

from share.models import FileModel
from share.utility.auth import protected



class ListOfFiles(APIView):

    @protected
    def get(self, request):
        user_obj = request.user
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
