from rest_framework.views import APIView
from django.http import JsonResponse, HttpResponse
from share.models import FileModel, ShareModel
from share.utility.auth import protected, deprecated
from cryptography.fernet import Fernet, InvalidToken
import base64
from share.utility import padding
import os


class FileDownloadAPIV3(APIView):
    """
    This is the update File Download API
    It decrypts the file at the server end and then returns the decrypted file.

    Args:
        APIView (_type_): _description_

    Returns:
        _type_: _description_
    """

    REQUIRED_PARAM = ("password",)

    @protected
    def post(self, request, file_id):
        data = request.data

        if "password" not in data:
            return JsonResponse({
                "message": "Missing decryption password!"
            }, status=400)

        password = data["password"]

        owner = request.user
        try:
            file_obj = FileModel.objects.get(index=file_id)
        except FileModel.DoesNotExist:
            return JsonResponse({
                "message": "File doesn't exist!"
            }, status=404)

        if file_obj.file_owner.pk != owner.pk:
            # check if the file is shared with him
            try:
                ShareModel.objects.get(
                    file=file_obj.pk, shared_with=owner.pk)
            except ShareModel.DoesNotExist:
                return JsonResponse({
                    "message": "You are not allowed to download this file!"
                }, status=403)

        filepath = file_obj.encrypted_data # todo: check if file exist.
        
        if not os.path.isfile(filepath):
            return JsonResponse({
                "message": "File doesn't exist anymore!"
            }, status=404)
        
        fernet_key = base64.urlsafe_b64encode(padding(password.encode()))
        f = Fernet(fernet_key)

        # Read the encrypted file from disk
        with open(filepath, 'rb') as file:
            encrypted_data = file.read()

        # Decrypt the file data using the Fernet key
        try:
            decrypted_data = f.decrypt(encrypted_data)
        except InvalidToken:
            return JsonResponse({
                "message": "Decryption Failed! Invalid password"
            }, status=401)

        # Serve the decrypted file as a response
        response = HttpResponse(content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{file_obj.original_filename}"'
        response.write(decrypted_data)
        return response


class FileDownloadAPIv2(APIView):

    @deprecated
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
