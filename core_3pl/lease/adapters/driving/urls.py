from django.urls import path
from .views import CreateQuote, ActivateLease

urlpatterns = [
    path("create-quote/", CreateQuote.as_view()),
    path("<uuid:lease_id>/activate/", ActivateLease.as_view())
]
