from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.ingestion.models import IngestionRun
from apps.ingestion.services import fetch_github_ai_projects
from apps.startups.models import Startup


class Command(BaseCommand):
    help = "Ingest projects from GitHub AI topic page"

    def handle(self, *args, **kwargs):
        run = IngestionRun.objects.create(source="ph", status="running")

        try:
            startups = fetch_github_ai_projects()
            created = 0

            for item in startups:
                _, was_created = Startup.objects.get_or_create(
                    external_id=item["external_id"],
                    source=item["source"],
                    defaults=item,
                )
                if was_created:
                    created += 1

            run.status = "success"
            run.fetched_count = len(startups)
            run.created_count = created
            run.finished_at = timezone.now()
            run.save()

            self.stdout.write(self.style.SUCCESS(f"Fetched: {len(startups)}"))
            self.stdout.write(self.style.SUCCESS(f"Created: {created}"))

        except Exception as exc:
            run.status = "failed"
            run.error_message = str(exc)
            run.finished_at = timezone.now()
            run.save()
            raise