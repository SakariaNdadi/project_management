from django.db.models import Q
from .models import Project


def user_projects(request):
    if request.user.is_authenticated:
        user = request.user
        projects = Project.objects.filter(Q(lead=user) | Q(members=user)).distinct()
    else:
        projects = (
            Project.objects.none()
        )  # Return an empty queryset for anonymous users

    return {"user_projects": projects}
