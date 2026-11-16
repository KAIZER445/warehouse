from django.urls import path

from .views import InventoryPosts

urlpatterns = [
    path("posts/", InventoryPosts.as_view()),
]
