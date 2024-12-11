from django.core.cache import cache
from .models import ProjectSettings


def global_variables(request):
    # Try to get cached value
    cached_variables = cache.get("project_settings")

    if cached_variables:
        return cached_variables

    # If not cached, fetch from database
    try:
        settings = ProjectSettings.objects.first()
        project_logo = settings.logo.url if settings and settings.logo else None
        project_name = settings.project_name if settings else "Scrum-ish"

        # Cache the result for future requests
        cache.set(
            "project_settings",
            {
                "project_logo": project_logo,
                "project_name": project_name,
            },
            timeout=60 * 15,
        )  # Cache for 15 minutes

        return {
            "project_logo": project_logo,
            "project_name": project_name,
        }
    except ProjectSettings.DoesNotExist:
        # If no settings exist, return default values
        return {
            "project_logo": None,
            "project_name": None,
        }
