from django.urls import path
from capacity.adapters.driving.views import GetCapacity

urlpatterns = [
    path("get/", GetCapacity.as_view())
]
