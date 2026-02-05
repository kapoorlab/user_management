"""URL configuration for NeuroAI Lab User Management project."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("src.urls")),
]
