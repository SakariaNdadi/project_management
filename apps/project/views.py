from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.http import (
    HttpResponse,
)
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from .models import (
    Project,
    Issue,
    Sprint,
    Epic,
    UserStory,
    AcceptanceCriteria,
    Categories,
    ProjectType,
)
from .forms import (
    ProjectForm,
    IssueForm,
    SprintForm,
    EpicForm,
    UserStoryForm,
    AcceptanceCriteriaForm,
)


# Project Views
def project_list(request) -> HttpResponse:
    user = request.user
    # projects = Project.objects.all()
    projects = Project.objects.filter(Q(lead=user) | Q(members=user)).distinct()
    return render(request, "project/list.html")


import json


def project_detail(request, pk) -> HttpResponse:
    user = request.user
    categories = Categories.choices
    project_types = ProjectType.choices
    project = get_object_or_404(Project, Q(pk=pk) & (Q(lead=user) | Q(members=user)))

    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect("project_list")
            # return redirect("project_detail", pk=project.pk)
    else:
        form = ProjectForm(instance=project)

    return render(
        request,
        "project/detail.html",
        {
            "form": form,
            "project": project,
            "categories": categories,
            "project_types": project_types,
        },
    )


class ProjectUpdateView(UpdateView):
    model = Project
    # form_class = ProjectForm
    fields = (
        "name",
        "type",
        "description",
        "start_date",
        "end_date",
        "lead",
        "members",
        "category",
        "is_active",
    )
    template_name = "project/detail.html"
    success_url = reverse_lazy("project_list")

    # def get_success_url(self):
    #     return reverse_lazy("project_detail", kwargs={"pk": self.object.pk})

    def get_object(self, queryset=None):
        user = self.request.user
        project = get_object_or_404(Project, Q(lead=user) | Q(members=user))
        return project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "categories": Categories.choices,
                "project_types": ProjectType.choices,
            }
        )
        return context


def project_create(
    request,
) -> HttpResponse:
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("project_list")
    else:
        form = ProjectForm()
    return render(request, "project/create.html", {"form": form})


def project_update(request, pk) -> HttpResponse:
    project = get_object_or_404(Project, pk=pk)
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("project_list")
    else:
        form = ProjectForm()
    return render(request, "project/update.html", {"form": form})


def project_delete(request, pk) -> HttpResponse:
    project = get_object_or_404(Project, pk=pk)
    project.delete()
    return redirect("project_list")


# Issue Views
def issue_create(request, project_pk):
    project = get_object_or_404(Project, pk=project_pk)
    if request.method == "POST":
        form = IssueForm(request.POST)
        if form.is_valid():
            issue = form.save(commit=False)
            issue.project = project
            issue.save()
            return redirect("project_detail", pk=project.pk)
    else:
        form = IssueForm()
    return render(
        request, "project/issues/create.html", {"form": form, "project": project}
    )


# Sprint Views
def sprint_create(request, project_pk):
    project = get_object_or_404(Project, pk=project_pk)
    if request.method == "POST":
        form = SprintForm(request.POST)
        if form.is_valid():
            sprint = form.save(commit=False)
            sprint.project = project
            sprint.save()
            return redirect("project_detail", pk=project.pk)
    else:
        form = SprintForm()
    return render(
        request, "project/sprints/create.html", {"form": form, "project": project}
    )


# Epic Views
def epic_create(request, project_pk):
    project = get_object_or_404(Project, pk=project_pk)
    if request.method == "POST":
        form = EpicForm(request.POST)
        if form.is_valid():
            epic = form.save(commit=False)
            epic.project = project
            epic.save()
            return redirect("project_detail", pk=project.pk)
    else:
        form = EpicForm()
    return render(
        request, "project/epics/create.html", {"form": form, "project": project}
    )


# User Story Views
def user_story_create(request, project_pk):
    project = get_object_or_404(Project, pk=project_pk)
    if request.method == "POST":
        form = UserStoryForm(request.POST)
        if form.is_valid():
            user_story = form.save(commit=False)
            user_story.project = project
            user_story.save()
            return redirect("project_detail", pk=project.pk)
    else:
        form = UserStoryForm()
    return render(
        request,
        "project/user_stories/create.html",
        {"form": form, "project": project},
    )


# Acceptance Criteria Views
def acceptance_criteria_create(request, user_story_pk):
    user_story = get_object_or_404(UserStory, pk=user_story_pk)
    if request.method == "POST":
        form = AcceptanceCriteriaForm(request.POST)
        if form.is_valid():
            acceptance_criteria = form.save(commit=False)
            acceptance_criteria.user_story = user_story
            acceptance_criteria.save()
            return redirect("user_story_detail", pk=user_story.pk)
    else:
        form = AcceptanceCriteriaForm()
    return render(
        request,
        "project/acceptance_criteria/create.html",
        {"form": form, "user_story": user_story},
    )


def project_members_list(request, project_id) -> HttpResponse:
    user = request.user
    project = get_object_or_404(
        Project, Q(pk=project_id) & (Q(lead=user) | Q(members=user))
    )
    context = {"project": project}
    return render(request, "project/members_list.html", context)


def project_epics_list(request, project_id) -> HttpResponse:
    user = request.user
    project = get_object_or_404(
        Project, Q(pk=project_id) & (Q(lead=user) | Q(members=user))
    )
    epics = Epic.objects.filter(project=project)
    context = {"epics": epics}
    return render(request, "project/epic_list.html", context)


def project_issues_list(request, project_id) -> HttpResponse:
    user = request.user
    project = get_object_or_404(
        Project, Q(pk=project_id) & (Q(lead=user) | Q(members=user))
    )
    issues = Issue.objects.filter(project=project)
    context = {"issues": issues}
    return render(request, "project/issue_list.html", context)
