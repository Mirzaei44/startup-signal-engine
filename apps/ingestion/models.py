
from django.db import models


class IngestionRun(models.Model):
    SOURCE_CHOICES = [
        ("hn", "HackerNews"),
        ("ph", "GitHub AI"),
        ("all", "All Sources"),
    ]

    source = models.CharField(max_length=20, choices=SOURCE_CHOICES)
    status = models.CharField(max_length=20, default="running")
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    fetched_count = models.IntegerField(default=0)
    created_count = models.IntegerField(default=0)
    error_message = models.TextField(blank=True)

    def __str__(self):
        return f"{self.source} - {self.status} - {self.started_at}"