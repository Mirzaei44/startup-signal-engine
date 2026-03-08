from django.urls import path
from .views import RunIngestionView

urlpatterns = [
    path("run/", RunIngestionView.as_view()),
]