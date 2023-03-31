from django.urls import path
from share.api.file_upload import FileUploadAPI

urlpatterns = [
    path('upload/', FileUploadAPI.as_view()),
]