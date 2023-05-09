from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import JsonResponse
from share.serializer import UploadSerializer, ShareSerializer
from user.models import User
from share.utility.auth import protected
from share.utility import check_password


class FileUploadAPI(APIView):

    parser_classes = (MultiPartParser, FormParser)
    REQUIRED_PARAMETERS = ("file", "filename", "password")
    OPTIONAL_PARAMETERS = ("shared_email", "file_type",)

    @protected
    def post(self, request):
        data = request.data

        for item in self.REQUIRED_PARAMETERS:
            if item not in data:
                return JsonResponse({
                    "message": "Missing required field {}".format(item)
                }, status=400)

        password = data.get("password")
        shared_with = data.get("shared_email", None)
        file_type = data.get("file_type", "")
        owner_obj = request.user
        print(password)
        if not check_password(password):
            return JsonResponse({
                "message": "Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one digit, and one special character."
            }, status=400)

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

        serializer_payload = {}
        serializer_payload["encrypted_data"] = None
        serializer_payload["original_filename"] = data['filename']
        serializer_payload["file_owner"] = owner_obj.pk
        serializer_payload["file_type"] = file_type

        upload_serializer = UploadSerializer(data=serializer_payload)
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
