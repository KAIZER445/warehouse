from django.urls import path

from .views import inventoryPosts

urlpatterns = [
    path("posts/", inventoryPosts.as_view()),
]
