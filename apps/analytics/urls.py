from django.urls import path
from .views import AnalyticsSummaryView, IngestionStatusView

urlpatterns = [
    path("summary/", AnalyticsSummaryView.as_view()),
     path("ingestion-status/", IngestionStatusView.as_view()),
]