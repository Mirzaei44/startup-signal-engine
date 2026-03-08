from celery import shared_task
from django.core.management import call_command


@shared_task
def ingest_all_sources():
    call_command("ingest_all")