from django.db import models


class Startup(models.Model):

    SOURCE_CHOICES = [
        ("hn", "HackerNews"),
        ("yc", "YCombinator"),
        ("ph", "ProductHunt"),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    website = models.URLField(blank=True)

    category = models.CharField(max_length=100, blank=True)

    source = models.CharField(max_length=20, choices=SOURCE_CHOICES)
    source_url = models.URLField(blank=True)

    external_id = models.CharField(max_length=100, blank=True)

    author = models.CharField(max_length=120, blank=True)

    score = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)

    posted_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name