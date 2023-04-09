from rest_framework.views import APIView
from django.http import JsonResponse
from share.models import FileModel
from user.models import User
from django.conf import settings
import os


class FileRemoveAPI(APIView):
    REQUIRED_PARAMETERS = ["file_id", ]

    def delete(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({
                "message": "Invalid Request!"
            }, status=400)

        data = request.data
        if 'file_id' not in data:
            return JsonResponse({
                "message": "Required parameter `file_id` is missing!"
            }, status=400)

        original_filename = None
        try:
            file_obj = FileModel.objects.get(index=data["file_id"])
            original_filename = file_obj.original_filename
        except FileModel.DoesNotExist:
            return JsonResponse({
                "status": "File Doesn't exist!"
            }, status=404)

        if file_obj.file_owner.pk != user.pk:
            return JsonResponse({
                "message": "You aren't allowed to perform this action!"
            }, status=403)

        try:
            file_path = os.path.join(settings.MEDIA_ROOT, file_obj.file.path)
            os.remove(file_path)
        except FileNotFoundError:
            # This exception has been added to minimize any critical crash.
            # File might go missing/delete
            # File was deleted during dev anyway
            pass

        status = os.path.isfile(file_path)  # this should be False, log this.
        print("File status: ", status == False)

        file_obj.delete()

        return JsonResponse({
            "message": "File {} removed successfully!".format(original_filename)
        }, status=202)
