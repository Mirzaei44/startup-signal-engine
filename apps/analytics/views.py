from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.ingestion.models import IngestionRun
from apps.startups.models import Startup


class AnalyticsSummaryView(APIView):

    def get(self, request):

        total = Startup.objects.count()

        by_source = (
            Startup.objects
            .values("source")
            .annotate(count=Count("id"))
            .order_by("-count")
        )

        latest = (
            Startup.objects
            .order_by("-created_at")[:10]
            .values("name", "source", "website")
        )

        top = (
            Startup.objects
            .order_by("-score", "-comments_count")[:10]
            .values("name", "score", "comments_count")
        )

        return Response({
            "total_startups": total,
            "sources": list(by_source),
            "latest": list(latest),
            "top_discussed": list(top),
        })
        
class IngestionStatusView(APIView):

    def get(self, request):
        latest_runs = IngestionRun.objects.order_by("-started_at")[:10]

        data = [
            {
                "source": run.source,
                "status": run.status,
                "started_at": run.started_at,
                "finished_at": run.finished_at,
                "fetched_count": run.fetched_count,
                "created_count": run.created_count,
                "error_message": run.error_message,
            }
            for run in latest_runs
        ]

        return Response(data)