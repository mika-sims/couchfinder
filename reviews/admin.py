from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "profile",
        "created_at",
        "updated_at",
    )

    ordering = ("-created_at",)
