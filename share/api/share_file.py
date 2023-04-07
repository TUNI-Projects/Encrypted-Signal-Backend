from django.http import JsonResponse
from rest_framework.views import APIView
from share.serializer import ShareSerializer
from share.models import ShareModel, FileModel
from user.models import User


class ShareAPI(APIView):

    REQUIRED_PARAMETERS = ("share_email", "file_id",)

    def post(self, request, username):
        data = request.data

        for item in self.REQUIRED_PARAMETERS:
            if item not in data:
                return JsonResponse({
                    "message": "Missing required field `{}`".format(item)
                }, status=400)

        try:
            curr_usr_obj = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({
                "message": "Invalid Request."
            }, status=403)

        try:
            file_obj = FileModel.objects.get(index=data["file_id"])
        except FileModel.DoesNotExist:
            return JsonResponse({
                "message": "File Does not exist!"
            }, status=404)

        if file_obj.file_owner.email != curr_usr_obj.email:
            return JsonResponse({
                "message": "You aren't allowed to share this file!"
            }, status=401)

        try:
            share_user = User.objects.get(email=data["share_email"])
        except User.DoesNotExist:
            return JsonResponse({
                "message": "User with email `{}` doesn't exist!".format(data["share_email"])
            }, status=404)

        try:
            share_obj = ShareModel.objects.get(
                file=file_obj.pk, shared_with=share_user.pk)
            print(share_obj)

            return JsonResponse({
                "message": "This file `{}` is already shared with `{}`".format(file_obj.original_filename, data["share_email"])
            }, status=400)
        except ShareModel.DoesNotExist:
            # all good. not previously shared
            pass

        payload = {
            "file": file_obj.pk,
            "shared_with": share_user.pk,
        }

        share_serializer = ShareSerializer(data=payload)
        if share_serializer.is_valid():
            share_serializer.save()
            return JsonResponse({
                "message": "File `{}` is successfully shared with `{}`".format(file_obj.original_filename, data["share_email"])
            }, status=202)
        else:
            print(share_serializer.errors)
            return JsonResponse({
                "message": "An error occurred while trying to share the file."
            }, status=400)
