from django.test import TestCase
from rest_framework.test import APIClient

from .models import Startup


class StartupTests(TestCase):

    def setUp(self):
        self.client = APIClient()

        Startup.objects.create(
            name="Startup A",
            source="hn",
            description="test",
            score=5,
            comments_count=3,
        )

    def test_trending_endpoint(self):
        response = self.client.get("/api/startups/trending/")

        self.assertEqual(response.status_code, 200)