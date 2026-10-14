from django.urls import path
from capacity.adapters.driving.views import GetCapacity, UpdateAllocatedSpace

urlpatterns = [
    path("get/", GetCapacity.as_view()),
    path("update-allocated-space/", UpdateAllocatedSpace.as_view())
]
