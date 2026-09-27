from django.urls import path
from .views import ListUsers, RegisterUser

urlpatterns = [
    path('list/', ListUsers.as_view()),
    path('register/', RegisterUser.as_view())
]
