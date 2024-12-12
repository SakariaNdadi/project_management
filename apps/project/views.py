from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.http import (
    HttpResponse,
)
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from .models import (
    Project,
    Issue,
    Sprint,
    Epic,
    UserStory,
    AcceptanceCriteria,
    Roles,
    ProjectMember,
    Status,
    Priority,
)
from .forms import (
    ProjectForm,
    IssueForm,
    SprintForm,
    EpicForm,
    UserStoryForm,
    AcceptanceCriteriaForm,
    InvitationForm,
)
from django.contrib.auth import get_user_model
from .emails import project_invitation_email

User = get_user_model()


# Project Views
def project_list(request) -> HttpResponse:
    user = request.user
    # projects = Project.objects.all()
    projects = Project.objects.filter(Q(lead=user) | Q(members=user)).distinct()
    return render(request, "project/list.html")


def project_detail(request, pk) -> HttpResponse:
    user = request.user
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


class ProjectCreateView(CreateView):
    model = Project
    fields = (
        "name",
        "description",
        "start_date",
        "end_date",
        "is_active",
    )
    template_name = "project/create.html"
    success_url = reverse_lazy("project_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "users": User.objects.all(),
            }
        )
        return context

    def form_valid(self, form) -> HttpResponse:
        form.instance.lead = self.request.user
        form.instance.created_by = self.request.user
        return super().form_valid(form)


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
def issue_create(request, project_id):
    user = request.user
    project = get_object_or_404(Project, pk=project_id)
    types = Issue.IssueType.choices
    statuses = Status.choices
    priorities = Priority.choices
    if request.method == "POST":
        form = IssueForm(request.POST)
        if form.is_valid():
            issue = form.save(commit=False)
            issue.project = project
            issue.created_by = user
            issue.save()
            return redirect("project_detail", pk=project.pk)
    else:
        form = IssueForm()
    return render(
        request,
        "project/issue/create.html",
        {
            "form": form,
            "project": project,
            "types": types,
            "statuses": statuses,
            "priorities": priorities,
        },
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
    roles = Roles.choices
    context = {"project": project, "roles": roles}
    return render(request, "project/members_list.html", context)


def project_epics_list(request, project_id) -> HttpResponse:
    user = request.user
    project = get_object_or_404(
        Project, Q(pk=project_id) & (Q(lead=user) | Q(members=user))
    )
    epics = Epic.objects.filter(project=project)
    context = {"epics": epics}
    return render(request, "project/epic/list.html", context)


def project_epics_detail(request, project_id, epic_id) -> HttpResponse:
    user = request.user
    project = get_object_or_404(
        Project, Q(pk=project_id) & (Q(lead=user) | Q(members=user))
    )
    epic = get_object_or_404(Epic, Q(project=project_id) & Q(pk=epic_id))
    context = {"epic": epic}
    return render(request, "project/epic/detail.html", context)


def project_issues_list(request, project_id) -> HttpResponse:
    user = request.user
    project = get_object_or_404(
        Project, Q(pk=project_id) & (Q(lead=user) | Q(members=user))
    )
    issues = Issue.objects.filter(project=project)
    context = {"issues": issues, "project": project}
    return render(request, "project/issue/list.html", context)


def project_member_invite(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect("project_list")
    else:
        form = ProjectForm(instance=project)


def invite_member(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == "POST":
        form = InvitationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            role = form.cleaned_data["role"]
            invitation_link = request.build_absolute_uri(
                f"/projects/{project.id}/accept-invite/?email={email}&role={role}"
            )
            # Use the email utility function
            project_invitation_email(project, email, role, invitation_link)
            return HttpResponse("Invitation sent successfully!")
    else:
        form = InvitationForm()
    return render(request, "invite_member.html", {"form": form, "project": project})


def accept_invite(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    email = request.GET.get("email")
    role = request.GET.get("role")

    user = User.objects.filter(email=email).first()

    if user:
        # Add the user as a project member
        ProjectMember.objects.update_or_create(
            project=project,
            user=user,
            defaults={"role": role, "is_active": True},
        )
        return HttpResponse("You have successfully joined the project.")
    return HttpResponse("Invalid invitation link.")
