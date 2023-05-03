from django.urls import path
from share.api.file_upload import FileUploadAPI
from share.api.file_list import ListOfFiles
from share.api.share_file import ShareAPI
from share.api.file_download import FileDownloadAPIv2
from share.api.share_file_list import ShareFileListAPI
from share.api.file_remove import FileRemoveAPI

urlpatterns = [
    path('upload/', FileUploadAPI.as_view()),
    
    path('uploaded_files/', ListOfFiles.as_view()), # Changing the URL format.
    path('shared_files/', ShareFileListAPI.as_view()),
    
    path('delete_file/', FileRemoveAPI.as_view()),
    # v2
    path('download/v2/<str:file_id>/', FileDownloadAPIv2.as_view()),
    
    path('', ShareAPI.as_view()),
]
