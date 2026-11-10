"""Admin configuration for the auth_app."""

from django.contrib import admin

from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Shows user profiles in the admin interface."""

    list_display = ["user", "type"]
    list_filter = ["type"]
