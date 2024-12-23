from django.urls import path
from . import views

urlpatterns: list = [
    path("create/", views.project_create, name="project_create"),
    path("list/", views.project_list, name="project_list"),
    path("detail/<int:pk>", views.project_detail, name="project_detail"),
    path("delete/<int:pk>", views.project_delete, name="project_delete"),
    path(
        "members/<int:project_id>/",
        views.project_members_list,
        name="project_members_list",
    ),
    path(
        "epics/<int:project_id>/",
        views.project_epics_list,
        name="project_epics_list",
    ),
]
