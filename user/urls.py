from django.urls import path
from user.motherland.register import RegisterAPI
from user.motherland.login import LoginAPI
from user.motherland.logout import LogoutAPI

urlpatterns = [
    path('register/', RegisterAPI.as_view()),
    path('login/', LoginAPI.as_view()),
    path('logout/', LogoutAPI.as_view()),
]
