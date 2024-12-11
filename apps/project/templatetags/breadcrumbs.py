# your_app/templatetags/breadcrumbs.py
from django import template
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.utils.html import mark_safe
from ..models import Project

register = template.Library()


@register.simple_tag(takes_context=True)
def generate_breadcrumbs(context):
    """
    Generate breadcrumbs for the current view, showing the project and list pages like 'epics_list', 'issues_list'.
    When viewing a specific epic (or other items), show the corresponding list page as the last breadcrumb.
    """
    request = context["request"]
    breadcrumbs = [
        {
            "title": "Dashboard",
            "url": reverse("home"),  # Adjust 'home' to your main dashboard URL name
        }
    ]

    # Add the project to the breadcrumbs if the project_id is in the URL
    if "project_id" in request.resolver_match.kwargs:
        project_id = request.resolver_match.kwargs["project_id"]
        project = get_object_or_404(Project, pk=project_id)
        breadcrumbs.append(
            {
                "title": project.name,
                "url": reverse("project_detail", kwargs={"pk": project.id}),
            }
        )

    # Check if we're in the project epics list or a specific epic
    if (
        "epic_id" in request.resolver_match.kwargs
        or "epics_list" in request.resolver_match.url_name
    ):
        breadcrumbs.append(
            {
                "title": "Epics",
                "url": reverse("project_epics_list", kwargs={"project_id": project_id}),
            }
        )

    # Check if we're in the project issues list
    if "issues_list" in request.resolver_match.url_name:
        breadcrumbs.append(
            {
                "title": "Issues",
                "url": reverse(
                    "project_issues_list", kwargs={"project_id": project_id}
                ),
            }
        )

    # Check if we're in the project members list
    if "members_list" in request.resolver_match.url_name:
        breadcrumbs.append(
            {
                "title": "Members",
                "url": reverse(
                    "project_members_list", kwargs={"project_id": project_id}
                ),
            }
        )

    # Return the breadcrumb trail as HTML
    breadcrumb_html = '<nav class="hidden md:inline-block text-sm font-medium text-neutral-600 dark:text-neutral-300" aria-label="breadcrumb"><ol class="flex flex-wrap items-center gap-1">'

    for i, breadcrumb in enumerate(breadcrumbs):
        # Determine if the breadcrumb is the last one
        is_last = i == len(breadcrumbs) - 1
        active_class = (
            "font-bold text-neutral-900 dark:text-white"
            if is_last
            else "hover:text-neutral-900 dark:hover:text-white"
        )

        # Add the breadcrumb HTML
        breadcrumb_html += f"""
            <li class="flex items-center gap-1">
                <a href="{breadcrumb['url']}" class="{active_class}">{breadcrumb['title']}</a>
                {"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' stroke='currentColor' fill='none' stroke-width='2' class='size-4' aria-hidden='true'><path stroke-linecap='round' stroke-linejoin='round' d='m8.25 4.5 7.5 7.5-7.5 7.5' /></svg>" if not is_last else ""}
            </li>
        """

    breadcrumb_html += "</ol></nav>"
    return mark_safe(breadcrumb_html)
