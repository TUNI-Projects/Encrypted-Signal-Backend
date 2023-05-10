from django.urls import path
from user.motherland.register import RegisterAPI
from user.motherland.login import LoginAPI
from user.motherland.logout import LogoutAPI

urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(),  name='login'),
    path('logout/', LogoutAPI.as_view(),  name='logout'),
]
