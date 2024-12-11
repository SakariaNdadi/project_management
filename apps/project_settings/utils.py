# utils.py
from django.conf import settings
from django.apps import apps
from functools import lru_cache
from django.core.exceptions import AppRegistryNotReady


@lru_cache
def get_project_settings():
    if not apps.ready:  # Ensure the app registry is ready
        raise AppRegistryNotReady("Apps aren't loaded yet.")

    from .models import ProjectSettings  # Import here to avoid early evaluation

    settings_obj = ProjectSettings.objects.first()
    if settings_obj:
        return settings_obj
    return None
