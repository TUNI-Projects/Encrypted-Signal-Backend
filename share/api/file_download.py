from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from user.models import User
from share.models import FileModel, ShareModel
from wsgiref.util import FileWrapper



class FileDownloadAPI(APIView):
    
    def get(self, request, username, file_id):
        try:
            owner_obj = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({
                "message": "Invalid Request."
            }, status=403)
        
        try:
            file_obj = FileModel.objects.get(index = file_id)
        except FileModel.DoesNotExist:
            return JsonResponse({
                "message": "File doesn't exist!"
            }, status=404)
        
        if file_obj.file_owner.pk != owner_obj.pk:
            # check if the file is shared with him
            try:
                share_obj = ShareModel.objects.get(file=file_obj.pk, shared_with=owner_obj.pk)
            except ShareModel.DoesNotExist:
                return JsonResponse({
                "message": "You are not allowed to download this file!"
            }, status=403)
        
        file_handle = file_obj.file.path
        try:
            docu = open(file_handle, 'rb')
        except FileNotFoundError:
            return JsonResponse({
                "message": "File is not there where it was supposed to be!"
            }, status=500)
        response = HttpResponse(FileWrapper(docu)) # add content_type='application/msword' in the db first
        response['Content-Disposition'] = 'attachment; filename="%s"' % file_obj.original_filename
        return response
        
            