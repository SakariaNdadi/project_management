from datetime import datetime
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

from django.core.exceptions import ValidationError

User = get_user_model()


# Choices
class ProjectType(models.TextChoices):
    SCRUM = "SC", "Scrum"
    KANBAN = "KA", "Kanban"
    WATERFALL = "WF", "Waterfall"
    AGILE = "AG", "Agile"
    LEAN = "LE", "Lean"
    SIX_SIGMA = "SS", "Six Sigma"
    PRINCE2 = "P2", "PRINCE2"
    HYBRID = "HY", "Hybrid"
    CPM = "CP", "Critical Path Method"
    CCPM = "CC", "Critical Chain Project Management"
    XP = "XP", "Extreme Programming"
    APF = "AP", "Adaptive Project Framework"
    PMBOK = "PM", "PMBOK (Project Management Body of Knowledge)"
    EVENT_CHAIN = "EC", "Event Chain Methodology"
    FDD = "FD", "Feature-Driven Development"
    RAD = "RA", "Rapid Application Development"
    IPD = "IP", "Integrated Project Delivery"
    DESIGN_THINKING = "DT", "Design Thinking"


class Priority(models.TextChoices):
    LOW = "low", "Low"
    MEDIUM = "medium", "Medium"
    HIGH = "high", "High"
    CRITICAL = "critical", "Critical"


class Categories(models.TextChoices):
    SOFTWARE = "Software", "Software Development"
    MARKETING = "Marketing", "Marketing Campaigns"
    FINANCE = "Finance", "Financial Planning"
    OPERATIONS = "Operations", "Operations Management"
    HR = "HR", "Human Resources"
    SALES = "Sales", "Sales and CRM"
    IT = "IT", "IT Infrastructure"
    RESEARCH = "Research", "Research and Development"
    DESIGN = "Design", "Product or Graphic Design"
    EDUCATION = "Education", "Educational Projects"
    HEALTHCARE = "Healthcare", "Healthcare Services"
    CUSTOMER_SERVICE = "Customer Service", "Customer Support"
    LEGAL = "Legal", "Legal Projects"
    EVENTS = "Events", "Event Planning"
    CONSTRUCTION = "Construction", "Construction Projects"
    NON_PROFIT = "Non-Profit", "Non-Profit Initiatives"


class Status(models.TextChoices):
    TO_DO = "TO_DO", "To Do"
    IN_PROGRESS = "IN_PROGRESS", "In Progress"
    IN_REVIEW = "IN_REVIEW", "In Review"
    COMPLETED = "COMPLETED", "Completed"
    BLOCKED = "BLOCKED", "Blocked"


class Roles(models.TextChoices):
    PRODUCT_OWNER = "PRODUCT_OWNER", "Product Owner"
    SCRUM_MASTER = "SCRUM_MASTER", "Scrum Master"
    DEVELOPER = "DEVELOPER", "Developer"
    TESTER = "TESTER", "Tester"
    SCRIBE = "SCRIBE", "Scribe"
    GUEST = "GUEST", "Guest"


# Abstract Models
class TimeStampAndOwnerAbstract(models.Model):
    created_by = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, related_name="%(class)s_created"
    )
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class DurationAbstract(models.Model):
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    duration = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    def calculate_duration(self) -> int | None:
        if self.start_date and self.end_date:
            if self.end_date < self.start_date:
                raise ValidationError("End date must be after start date.")
            return (self.end_date - self.start_date).days
        return None

    class Meta:
        abstract = True


class Project(TimeStampAndOwnerAbstract, DurationAbstract):
    name = models.CharField(max_length=255, unique=True)
    type = models.CharField(max_length=3, choices=ProjectType.choices)
    description = models.TextField(
        blank=True, null=True, help_text="Project Description"
    )
    lead = models.ForeignKey(
        User,
        related_name="project_lead",
        null=True,
        on_delete=models.SET_NULL,
        help_text="The lead user managing the project",
    )
    members = models.ManyToManyField(
        User, related_name="project_member", through="ProjectMember"
    )
    category = models.CharField(max_length=20, choices=Categories.choices)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("project_detail", args=[self.pk])

    def save(self, *args, **kwargs) -> None:
        if self.start_date and self.end_date:
            self.duration = self.calculate_duration()
        super().save(*args, **kwargs)


class ProjectMember(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(
        max_length=15, choices=Roles.choices, default=Roles.DEVELOPER
    )
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("project", "user", "role")


class Issue(TimeStampAndOwnerAbstract, DurationAbstract):
    class IssueType(models.TextChoices):
        BUG = "BUG", "Bug"
        TASK = "TASK", "Task"
        FEATURE = "FEATURE", "Feature"
        IMPROVEMENT = "IMPROVEMENT", "Improvement"

    project = models.ForeignKey(
        Project, related_name="issues", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255, help_text="Issue title")
    description = models.TextField(
        blank=True, null=True, help_text="Detailed description of the issue"
    )
    type = models.CharField(
        max_length=20,
        choices=IssueType.choices,
        default=IssueType.TASK,
        help_text="Type of the issue (e.g., Bug, Task, Feature)",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.TO_DO,
        help_text="Current status of the issue",
    )
    priority = models.CharField(
        max_length=20,
        choices=Priority.choices,
        default=Priority.MEDIUM,
        help_text="Priority level of the issue",
    )
    assignee = models.ForeignKey(
        User,
        related_name="assigned_issues",
        null=True,
        on_delete=models.SET_NULL,
        help_text="User assigned to this issue",
    )
    resolution = models.TextField(
        blank=True, null=True, help_text="Resolution details once the issue is resolved"
    )

    # bug report
    steps_to_reproduce = models.TextField(
        blank=True, null=True, help_text="Steps to reproduce the bug"
    )
    expected_result = models.TextField(
        blank=True, null=True, help_text="What was expected to happen"
    )
    actual_result = models.TextField(
        blank=True, null=True, help_text="What actually happened"
    )
    environment = models.TextField(
        blank=True,
        null=True,
        help_text="Environment details (e.g., OS, browser version)",
    )

    # Feature-specific fields
    requirements = models.TextField(
        blank=True, null=True, help_text="Business requirements for the feature"
    )
    business_value = models.TextField(
        blank=True, null=True, help_text="The value this feature brings to the business"
    )
    feature_dependencies = models.TextField(
        blank=True,
        null=True,
        help_text="Other features, tasks, or issues this feature depends on",
    )

    # Improvement-specific fields
    performance_impact = models.TextField(
        blank=True, null=True, help_text="Impact of the improvement on performance"
    )
    estimated_impact = models.TextField(
        blank=True, null=True, help_text="Estimated improvement in performance"
    )
    user_feedback = models.TextField(
        blank=True, null=True, help_text="User feedback that led to this improvement"
    )
    technical_details = models.TextField(
        blank=True, null=True, help_text="Technical aspects of the improvement"
    )

    # Task-specific fields
    effort_estimate = models.PositiveIntegerField(
        blank=True, null=True, help_text="Estimated effort in hours/days"
    )
    dependent_on = models.ForeignKey(
        "self",
        related_name="issue_dependencies",
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        help_text="Dependencies on other tasks or issues",
    )

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs) -> None:
        if self.start_date and self.end_date:
            self.duration = self.calculate_duration()
        super().save(*args, **kwargs)

    class Meta:
        ordering: list[str] = ["-created_at"]


class IssueAttachment(TimeStampAndOwnerAbstract):
    issue = models.ForeignKey(
        Issue, on_delete=models.CASCADE, related_name="attachments"
    )
    file = models.FileField(upload_to="issues/attachments/")
    description = models.TextField(blank=True, null=True)


class Sprint(TimeStampAndOwnerAbstract, DurationAbstract):

    class SprintStatuses(models.TextChoices):
        NOT_STARTED = "NOT_STARTED", "Not Started"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        COMPLETED = "COMPLETED", "Completed"
        ARCHIVED = "ARCHIVED", "Archived"

    project = models.ForeignKey(
        Project, related_name="sprints", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255, help_text="Sprint name or title")
    goal = models.TextField(blank=True, null=True, help_text="Sprint goal or objective")
    status = models.CharField(
        max_length=20,
        choices=SprintStatuses.choices,
        default=SprintStatuses.NOT_STARTED,
        help_text="The current status of the sprint",
    )
    is_active = models.BooleanField(
        default=True, help_text="Whether the sprint is currently active"
    )
    completed_at = models.DateTimeField(
        blank=True, null=True, help_text="When the sprint was completed"
    )
    issues = models.ManyToManyField(
        Issue,
        blank=True,
        related_name="sprints",
        help_text="Issues assigned to this sprint",
    )

    def __str__(self) -> str:
        return f"Sprint: {self.name} ({self.project.name})"

    def save(self, *args, **kwargs) -> None:
        if self.start_date and self.end_date:
            self.duration = self.calculate_duration()
        super().save(*args, **kwargs)


class Epic(TimeStampAndOwnerAbstract, DurationAbstract):
    class EpicStatuses(models.TextChoices):
        TO_DO = "TO_DO", "To Do"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        COMPLETED = "COMPLETED", "Completed"
        ARCHIVED = "ARCHIVED", "Archived"

    project = models.ForeignKey(Project, related_name="epics", on_delete=models.CASCADE)
    title = models.CharField(max_length=255, help_text="Epic title or name")
    description = models.TextField(
        blank=True, null=True, help_text="Detailed description of the epic"
    )
    status = models.CharField(
        max_length=20,
        choices=EpicStatuses.choices,
        default=EpicStatuses.TO_DO,
        help_text="Current status of the epic",
    )
    priority = models.CharField(
        max_length=20,
        choices=Priority.choices,
        default=Priority.LOW,
        help_text="Priority of the epic",
    )
    completed_at = models.DateTimeField(
        null=True, blank=True, help_text="Epic completion date"
    )
    issues = models.ManyToManyField(
        Issue,
        blank=True,
        related_name="epics",
        help_text="Issues linked to this epic",
    )
    is_blocked = models.BooleanField(
        default=False, help_text="Whether the epic is currently blocked"
    )
    is_published = models.BooleanField(
        default=False, help_text="Whether the epic is currently published"
    )

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse(
            "project_epics_detail",
            kwargs={"project_id": self.project.pk, "epic_id": self.pk},
        )

    def save(self, *args, **kwargs) -> None:
        if self.start_date and self.end_date:
            self.duration = self.calculate_duration()
        super().save(*args, **kwargs)

    class Meta:
        ordering: list[str] = ["-created_at"]


class UserStory(TimeStampAndOwnerAbstract, DurationAbstract):
    title = models.CharField(
        max_length=255, help_text="The title or summary of the user story"
    )
    description = models.TextField(
        blank=True, null=True, help_text="Detailed description of the user story"
    )
    priority = models.CharField(
        max_length=20,
        choices=Priority.choices,
        default=Priority.LOW,
        help_text="Priority level of the user story",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.TO_DO,
        help_text="Current status of the user story",
    )
    is_active = models.BooleanField(
        default=True, help_text="Whether the user story is still active or completed"
    )
    is_blocked = models.BooleanField(
        default=False, help_text="Whether the user story is currently blocked"
    )
    epic = models.ForeignKey(
        Epic,
        related_name="user_stories",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="Epic to which this user story belongs",
    )
    sprint = models.ForeignKey(
        Sprint,
        related_name="user_stories",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="Sprint to which this user story is assigned",
    )
    issues = models.ManyToManyField(Issue, related_name="user_stories")

    product_owner = models.ForeignKey(
        User, on_delete=models.PROTECT, blank=True, null=True
    )
    is_approved = models.BooleanField(default=False)
    is_approved_datetime = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs) -> None:
        if self.start_date and self.end_date:
            self.duration = self.calculate_duration()
        if self.is_approved:
            self.is_approved_datetime = datetime.now()
        super().save(*args, **kwargs)

    class Meta:
        ordering: list[str] = ["-created_at"]
        verbose_name_plural = "User Stories"


class AcceptanceCriteria(TimeStampAndOwnerAbstract):
    class CriteriaType(models.TextChoices):
        BEHAVIOuR_DRIVEN = "BD", "Behaviour-Driven"
        DESCRIPTIVE = "DS", "Descriptive"

    user_story = models.ForeignKey(
        UserStory,
        on_delete=models.CASCADE,
        related_name="acceptance_criteria",
        blank=True,
        null=True,
    )
    issue = models.ForeignKey(
        Issue,
        on_delete=models.CASCADE,
        related_name="acceptance_criteria",
        blank=True,
        null=True,
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Detailed description of the acceptance criteria",
    )
    given = models.TextField(
        blank=True, null=True, help_text="The initial conditions or context (Given)."
    )
    when = models.TextField(
        blank=True,
        null=True,
        help_text="The event or action that triggers the behaviour (When).",
    )
    then = models.TextField(
        blank=True, null=True, help_text="The expected outcome or result (Then)."
    )
    type = models.CharField(
        max_length=2,
        choices=CriteriaType.choices,
        default=CriteriaType.BEHAVIOuR_DRIVEN,
        help_text="Type of acceptance criteria (Behaviour-Driven or Descriptive)",
    )
    is_met = models.BooleanField(
        default=False,
        help_text="Indicates whether the acceptance criteria has been met",
    )
    is_met_date = models.DateTimeField()

    def __str__(self) -> str:
        return f"Acceptance Criteria for {self.user_story.title}"

    def save(self) -> None:
        if self.is_met:
            self.is_met_date = datetime.now()

    class Meta:
        ordering: list[str] = ["-created_at"]


# *********************************************************************
# TESTER
# *********************************************************************


class TestLevels(models.TextChoices):
    COMPONENT = "COMPONENT", "Component"
    COMPONENT_INTEGRATION = "COMPONENT_INTEGRATION", "Component Integration"
    SYSTEM = "SYSTEM", "System"
    SYSTEM_INTEGRATION = "SYSTEM_INTEGRATION", "System Integration"
    ACCEPTANCE = "ACCEPTANCE", "Acceptance"


class TestTypes(models.TextChoices):
    FUNCTIONAL = "FUNCTIONAL", "Functional"
    NON_FUNCTIONAL = "NON_FUNCTIONAL", "Non-Functional"
    BLACK_BOX = "BLACK_BOX", "Black Box"
    WHITE_BOX = "WHITE_BOX", "White Box"
    CONFIRMATION = "CONFIRMATION", "Confirmation"
    REGRESSION = "REGRESSION", "Regression"
    MAINTENANCE = "MAINTENANCE", "Maintenance"


class AcceptanceTestingTypes(models.TextChoices):
    USER = "USER", "User"
    OPERATIONAL = "OPERATIONAL", "Operational"
    ALPHA = "ALPHA", "Alpha"
    BETA = "BETA", "Beta"


class TestCase(TimeStampAndOwnerAbstract):
    title = models.CharField(max_length=255, help_text="Title of the test case")
    description = models.TextField(
        blank=True, null=True, help_text="Detailed description of the test case"
    )
    steps = models.TextField(
        blank=True, null=True, help_text="Steps to execute the test case"
    )
    expected_result = models.TextField(
        blank=True, null=True, help_text="Expected result after test execution"
    )
    issue = models.ForeignKey(
        "Issue",
        related_name="test_cases",
        on_delete=models.CASCADE,
        help_text="Issue associated with this test case",
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering: list[str] = ["-created_at"]


class TestExecution(TimeStampAndOwnerAbstract):
    class ExecutionType(models.TextChoices):
        MANUAL = "MANUAL", "Manual"
        AUTOMATED = "AUTOMATED", "Automated"

    class ExecutionStatus(models.TextChoices):
        PASSED = "PASSED", "Passed"
        FAILED = "FAILED", "Failed"
        BLOCKED = "BLOCKED", "Blocked"
        NOT_EXECUTED = "NOT_EXECUTED", "Not Executed"

    test_case = models.ForeignKey(
        TestCase,
        related_name="executions",
        on_delete=models.CASCADE,
        help_text="Test case being executed",
    )
    execution_type = models.CharField(
        max_length=10,
        choices=ExecutionType.choices,
        default=ExecutionType.MANUAL,
        help_text="Type of execution (manual or automated)",
    )
    status = models.CharField(
        max_length=15,
        choices=ExecutionStatus.choices,
        default=ExecutionStatus.NOT_EXECUTED,
        help_text="Result of the test execution",
    )
    executed_by = models.ForeignKey(
        User,
        related_name="test_executions",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="User who executed the test case",
    )
    execution_date = models.DateTimeField(
        auto_now_add=True, help_text="When the test case was executed"
    )
    log = models.TextField(
        blank=True, null=True, help_text="Detailed log of the test execution"
    )
    attachments = models.FileField(
        upload_to="test_execution/attachments/",
        null=True,
        blank=True,
        help_text="Evidence or logs of the execution",
    )

    def __str__(self) -> str:
        return f"{self.test_case.title} - {self.execution_type}"

    class Meta:
        ordering: list[str] = ["-execution_date"]


class TestPlan(TimeStampAndOwnerAbstract, DurationAbstract):
    title = models.CharField(max_length=255, help_text="Title of the test plan")
    description = models.TextField(
        blank=True, null=True, help_text="Detailed description of the test plan"
    )

    # Test Approach
    entry_criteria = models.TextField(
        blank=True, null=True, help_text="Detailed description of the test plan"
    )
    exit_criteria = models.TextField(
        blank=True, null=True, help_text="Detailed description of the test plan"
    )
    test_cases = models.ManyToManyField(
        "TestCase",
        related_name="test_plans",
        help_text="Test cases included in this test plan",
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering: list[str] = ["-created_at"]
