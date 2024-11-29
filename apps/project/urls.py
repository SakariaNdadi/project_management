from django.urls import path
from . import views

urlpatterns: list = [
    path("create/", views.project_create, name="project_create"),
    path("list/", views.project_list, name="project_list"),
    path("detail/<int:pk>", views.project_detail, name="project_detail"),
    path("delete/<int:pk>", views.project_delete, name="project_delete"),
]
