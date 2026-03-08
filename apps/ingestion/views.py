from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone

from apps.ingestion.tasks import ingest_all_sources


class RunIngestionView(APIView):
    def post(self, request):
        task = ingest_all_sources.delay()

        return Response({
            "status": "queued",
            "task_id": str(task.id),
            "queued_at": timezone.now(),
        })