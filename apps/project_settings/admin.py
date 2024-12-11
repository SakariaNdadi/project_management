from django.contrib import admin
from .models import ProjectSettings


@admin.register(ProjectSettings)
class ProjectSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Prevent adding multiple instances
        return not ProjectSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Prevent deleting the singleton
        return False
