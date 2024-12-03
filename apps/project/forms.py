from django import forms
from .models import Project, Issue, Sprint, Epic, UserStory, AcceptanceCriteria


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = (
            "name",
            "type",
            "description",
            "start_date",
            "end_date",
            "category",
            "is_active",
        )


class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = "__all__"


class SprintForm(forms.ModelForm):
    class Meta:
        model = Sprint
        fields = "__all__"


class EpicForm(forms.ModelForm):
    class Meta:
        model = Epic
        fields = "__all__"


class UserStoryForm(forms.ModelForm):
    class Meta:
        model = UserStory
        fields = "__all__"


class AcceptanceCriteriaForm(forms.ModelForm):
    class Meta:
        model = AcceptanceCriteria
        fields = "__all__"
