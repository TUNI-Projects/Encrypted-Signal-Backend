from django.urls import path
from share.api.file_upload import FileUploadAPI
from share.api.file_list import ListOfFiles

urlpatterns = [
    path('upload/', FileUploadAPI.as_view()),
    path('uploaded_files/<str:username>/', ListOfFiles.as_view()),
]