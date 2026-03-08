from django.contrib import admin
from .models import Startup


@admin.register(Startup)
class StartupAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "category",
        "source",
        "created_at",
    )

    search_fields = (
        "name",
        "description",
    )