from django.urls import path
from share.api.file_upload import FileUploadAPI
from share.api.file_list import ListOfFiles
from share.api.share_file import ShareAPI

urlpatterns = [
    path('upload/<str:username>/', FileUploadAPI.as_view()),
    path('uploaded_files/<str:username>/', ListOfFiles.as_view()),
    path('<str:username>/', ShareAPI.as_view()),
]