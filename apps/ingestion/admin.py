from django.contrib import admin
from .models import IngestionRun


@admin.register(IngestionRun)
class IngestionRunAdmin(admin.ModelAdmin):
    list_display = (
        "source",
        "status",
        "fetched_count",
        "created_count",
        "started_at",
        "finished_at",
    )
    list_filter = ("source", "status")