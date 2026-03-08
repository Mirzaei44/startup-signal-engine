# apps/startups/views.py

from datetime import timedelta

from django.db.models import F, ExpressionWrapper, FloatField
from django.utils import timezone

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Startup
from .serializers import StartupSerializer


class StartupViewSet(viewsets.ModelViewSet):

    queryset = Startup.objects.all()
    serializer_class = StartupSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    filterset_fields = ["source", "category"]
    search_fields = ["name", "description", "category"]
    ordering_fields = ["created_at", "name", "score", "comments_count"]
    ordering = ["-created_at"]

    @action(detail=False, methods=["get"])
    def trending(self, request):

        recent_time = timezone.now() - timedelta(days=3)

        qs = (
            Startup.objects.filter(created_at__gte=recent_time)
            .annotate(
                trend_score=ExpressionWrapper(
                    F("score") * 2 + F("comments_count") * 3,
                    output_field=FloatField(),
                )
            )
            .order_by("-trend_score")[:20]
        )

        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)