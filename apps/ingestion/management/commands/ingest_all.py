from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.ingestion.models import IngestionRun


class Command(BaseCommand):
    help = "Ingest all configured startup sources"

    def handle(self, *args, **kwargs):
        run = IngestionRun.objects.create(source="all", status="running")

        try:
            call_command("ingest_hn")
            call_command("ingest_yc")

            run.status = "success"
            run.finished_at = timezone.now()
            run.save()

            self.stdout.write(self.style.SUCCESS("All sources ingested."))

        except Exception as exc:
            run.status = "failed"
            run.error_message = str(exc)
            run.finished_at = timezone.now()
            run.save()
            raise