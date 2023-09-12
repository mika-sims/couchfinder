from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Custom Profile model admin.
    """
    list_display = ('user', 'couch_status')
    list_filter = ('user',)
    search_fields = ('user',)
    ordering = ('user',)
    filter_horizontal = ()

