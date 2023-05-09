from rest_framework.views import APIView
from django.http import JsonResponse
from share.models import ShareModel
from share.utility.auth import protected


class ShareFileListAPI(APIView):

    @protected
    def get(self, request):
        # sends all the files shared with this user.
        user_obj = request.user
        all_shared_file = list(
            ShareModel.objects.filter(shared_with=user_obj.pk))
        payload = list()

        for shared_file in all_shared_file:
            payload.append({
                "file_id": shared_file.file.index,
                "original_filename": shared_file.file.original_filename,
                "shared_by": shared_file.file.file_owner.email,
                "file_type": shared_file.file.file_type,
                "uploaded_at": shared_file.file.uploaded_at,
                "shared_at": shared_file.shared_on,
            })
        return JsonResponse({
            "shared_files": payload
        }, status=200)
