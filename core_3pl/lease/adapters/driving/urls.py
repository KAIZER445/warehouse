from django.urls import path
from .views import CreateQuote, ActivateLease, DemoSignalView

urlpatterns = [
    path("create-quote/", CreateQuote.as_view()),
    path("<uuid:lease_id>/activate/", ActivateLease.as_view()),
    path("test/", DemoSignalView.as_view())
]
