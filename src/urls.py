from django.urls import include, path

from . import views

urlpatterns = [
    # Dashboard
    path("", views.dashboard, name="dashboard"),
    # Toolkits
    path("toolkits/", views.toolkit_list, name="toolkit_list"),
    path("toolkit/<slug:slug>/", views.toolkit_detail, name="toolkit_detail"),
    # Studios
    path("studios/", views.studio_list, name="studio_list"),
    path("studio/<slug:slug>/", views.studio_detail, name="studio_detail"),
    # Workflows
    path(
        "studio/<slug:studio_slug>/workflow/<slug:workflow_slug>/",
        views.workflow_detail,
        name="workflow_detail",
    ),
    # Datasets
    path("datasets/", views.dataset_list, name="dataset_list"),
    path("dataset/<slug:slug>/", views.dataset_detail, name="dataset_detail"),
    # Authentication
    path("accounts/", include("django.contrib.auth.urls")),
    path("register/", views.register, name="register"),
]
