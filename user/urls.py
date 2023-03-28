from django.urls import path
from user.motherland.register import RegisterAPI

urlpatterns = [
    path('register/', RegisterAPI.as_view()),
]