from .models import ProjectSettings


def global_variables(request):
    try:
        settings = ProjectSettings.objects.first()
        return {
            "project_logo": settings.logo.url if settings and settings.logo else None,
            "project_name": settings.project_name if settings else "Scrum-ish",
        }
    except ProjectSettings.DoesNotExist:
        return {
            "project_logo": None,
            "project_name": None,
        }
