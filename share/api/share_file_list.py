from rest_framework.views import APIView
from django.http import JsonResponse
from share.models import ShareModel
from user.models import User


class ShareFileListAPI(APIView):

    def get(self, request, username):
        # sends all the files shared with this user.
        try:
            user_obj = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({
                "message": "Invalid Request!",
            }, status=404)

        all_shared_file = list(
            ShareModel.objects.filter(shared_with=user_obj.pk))
        payload = list()

        for shared_file in all_shared_file:
            payload.append({
                "file_id": shared_file.file.index,
                "original_filename": shared_file.file.original_filename,
                "shared_by": shared_file.file.file_owner.email,
                "file_type": shared_file.file.file_type,
                "uploaded_on": shared_file.file.uploaded_at,
                "shared_on": shared_file.shared_on,
            })
        return JsonResponse({
            "shared_files": payload
        }, status=200)
