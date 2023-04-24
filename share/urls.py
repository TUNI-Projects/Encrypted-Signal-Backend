from django.urls import path
from share.api.file_upload import FileUploadAPI
from share.api.file_list import ListOfFiles
from share.api.share_file import ShareAPI
from share.api.file_download import FileDownloadAPI, FileDownloadAPIv2
from share.api.share_file_list import ShareFileListAPI
from share.api.file_remove import FileRemoveAPI

urlpatterns = [
    path('upload/<str:username>/', FileUploadAPI.as_view()),
    
    path('uploaded_files/<str:username>/', ListOfFiles.as_view()),
    path('shared_files/<str:username>/', ShareFileListAPI.as_view()),
    
    path('delete_file/<str:username>/', FileRemoveAPI.as_view()),
    # v1
    path('download/<str:username>/<str:file_id>/', FileDownloadAPI.as_view()),
    # v2
    path('download/v2/<str:username>/<str:file_id>/', FileDownloadAPIv2.as_view()),
    
    path('<str:username>/', ShareAPI.as_view()),
]
