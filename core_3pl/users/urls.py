from django.urls import path
from .views import ListUsers

urlpatterns = [
    path('list/', ListUsers.as_view()),
]
