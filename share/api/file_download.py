from rest_framework.views import APIView
from django.http import JsonResponse
from share.models import FileModel, ShareModel
import base64
from share.utility.auth import protected


class FileDownloadAPIv2(APIView):

    @protected
    def get(self, request, file_id):
        owner_obj = request.user
        try:
            file_obj = FileModel.objects.get(index=file_id)
        except FileModel.DoesNotExist:
            return JsonResponse({
                "message": "File doesn't exist!"
            }, status=404)

        if file_obj.file_owner.pk != owner_obj.pk:
            # check if the file is shared with him
            try:
                share_obj = ShareModel.objects.get(
                    file=file_obj.pk, shared_with=owner_obj.pk)
            except ShareModel.DoesNotExist:
                return JsonResponse({
                    "message": "You are not allowed to download this file!"
                }, status=403)

        encrypted_data = file_obj.encrypted_data
        # why am I encoding and decoding??
        # base64_contents = base64.b64encode(
        #     encrypted_data.encode('utf-8')).decode('utf-8')
        response = {
            "filename": file_obj.original_filename,
            "content": encrypted_data,
            "file_type": file_obj.file_type,
        }
        return JsonResponse(response, status=200)
