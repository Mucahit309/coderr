"""Admin configuration for the profile_app."""

from django.contrib import admin

from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Shows user profiles in the admin interface."""

    list_display = ["user", "type", "location", "created_at"]
    list_filter = ["type"]
    search_fields = ["user__username", "first_name", "last_name"]
