from django.contrib import admin
from .forms import ProjectForm
from .models import (
    Project,
    Issue,
    Sprint,
    Epic,
    UserStory,
    AcceptanceCriteria,
    ProjectMember,
)


class ProjectMemberInline(admin.TabularInline):
    model = ProjectMember
    extra = 1  # Number of empty forms to display
    fields = ("user", "role", "is_active", "date_joined")  # Customize fields shown
    readonly_fields = ("date_joined",)  # Make date_joined read-only
    autocomplete_fields = ("user",)  # Enable autocomplete for User if applicable


# Register Project model
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "methodology",
        "category",
        "start_date",
        "end_date",
        "is_active",
        "created_by",
    )
    form = ProjectForm
    list_filter = ("methodology", "category", "is_active", "created_by")
    search_fields = ("name", "description")
    ordering = ("-created_at",)
    inlines = [ProjectMemberInline]


# Register Issue model
@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "project",
        "_type",
        "status",
        "priority",
        "assignee",
        "due_date",
        "created_at",
        "updated_at",
    )
    list_filter = ("_type", "status", "priority", "project", "assignee")
    search_fields = ("title", "description")
    ordering = ("-created_at",)


# Register Sprint model
@admin.register(Sprint)
class SprintAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "project",
        "start_date",
        "end_date",
        "goal",
        "status",
        "is_active",
        "created_at",
        "updated_at",
    )
    list_filter = ("status", "project", "is_active")
    search_fields = ("name", "goal")
    ordering = ("-created_at",)


# Register Epic model
@admin.register(Epic)
class EpicAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "project",
        "status",
        "priority",
        "start_date",
        "end_date",
        "is_active",
        "created_at",
        "updated_at",
    )
    list_filter = ("status", "priority", "project", "is_active")
    search_fields = ("title", "description")
    ordering = ("-created_at",)


# Register UserStory model
@admin.register(UserStory)
class UserStoryAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "priority",
        "status",
        "sprint",
        "due_date",
        "created_at",
        "updated_at",
    )
    list_filter = ("status", "priority", "sprint")
    search_fields = ("title", "description")
    ordering = ("-created_at",)


# Register AcceptanceCriteria model
@admin.register(AcceptanceCriteria)
class AcceptanceCriteriaAdmin(admin.ModelAdmin):
    list_display = (
        "user_story",
        "criteria_type",
        "is_met",
        "is_met_date",
        "created_at",
        "updated_at",
    )
    list_filter = ("criteria_type", "is_met", "user_story")
    search_fields = ("user_story__title", "description")
    ordering = ("-created_at",)
