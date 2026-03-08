from django.test import TestCase
from rest_framework.test import APIClient

from apps.startups.models import Startup


class AnalyticsTests(TestCase):

    def setUp(self):
        self.client = APIClient()

        Startup.objects.create(
            name="Test Startup",
            source="hn",
            description="test",
            score=10,
            comments_count=5,
        )

    def test_summary_endpoint(self):
        response = self.client.get("/api/analytics/summary/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("total_startups", response.data)