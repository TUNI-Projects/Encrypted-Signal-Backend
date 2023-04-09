from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import JsonResponse
from share.serializer import UploadSerializer, ShareSerializer
from user.models import User


class FileUploadAPI(APIView):

    parser_classes = (MultiPartParser, FormParser)
    REQUIRED_PARAMETERS = ("file",)
    OPTIONAL_PARAMETERS = ("shared_email", "file_type",)

    def post(self, request, username=None):
        data = request.data

        for item in self.REQUIRED_PARAMETERS:
            if item not in data:
                return JsonResponse({
                    "message": "Missing required field {}".format(item)
                }, status=400)

        shared_with = data.get("shared_email", None)
        file_type = data.get("file_type", "")
        original_filename = data['file']

        try:
            owner_obj = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({
                "message": "Invalid Request."
            }, status=403)

        shared_obj = None
        # this is optional
        if shared_with is not None:
            try:
                shared_obj = User.objects.get(email=shared_with)
            except User.DoesNotExist:
                return JsonResponse({
                    "message": "User with email address: `{}` does not exist!".format(shared_with)
                }, status=404)

            if owner_obj.pk == shared_obj.pk:
                # File Owner and Shared User are same.
                return JsonResponse({
                    "message": "You can't share this file with yourself."
                }, status=400)

        data["original_filename"] = original_filename.name
        data["file_owner"] = owner_obj.pk
        data["file_type"] = file_type

        upload_serializer = UploadSerializer(data=data)
        if upload_serializer.is_valid():
            res = upload_serializer.save()
            payload = {
                "message": "File Uploaded Successfully!"
            }

            # share with people if needed.
            if shared_obj is not None:
                share_serializer = ShareSerializer(data={
                    "file": res.pk,
                    "shared_with": shared_obj.pk,
                })
                if share_serializer.is_valid():
                    share_serializer.save()
                    payload["message"] = payload["message"] + \
                        " File Shared with `{}`".format(shared_with)
                else:
                    print(share_serializer.errors)
                    payload["message"] = payload["message"] + \
                        " Unabled to share with `{}` due to some internal error!".format(
                            shared_with)
                    payload["share_error"] = share_serializer.errors
            return JsonResponse(payload, status=201)
        else:
            return JsonResponse({
                "message": upload_serializer.errors,
            }, status=400)
