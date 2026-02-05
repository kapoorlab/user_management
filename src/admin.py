from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import Dataset, LabUser, Studio, Toolkit, Workflow


@admin.register(LabUser)
class LabUserAdmin(UserAdmin):
    """Admin for custom LabUser model."""

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = LabUser
    list_display = (
        "username",
        "email",
        "uni_email",
        "supervisor",
        "project_start_date",
        "is_staff",
    )
    list_filter = ("is_staff", "is_active", "supervisor")
    search_fields = (
        "username",
        "email",
        "uni_email",
        "first_name",
        "last_name",
    )
    ordering = ("username",)

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email")}),
        (
            "Lab Info",
            {
                "fields": (
                    "uni_email",
                    "github_username",
                    "basecamp_id",
                    "supervisor",
                    "project_start_date",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2"),
            },
        ),
        (
            "Lab Info",
            {
                "fields": (
                    "uni_email",
                    "github_username",
                    "basecamp_id",
                    "supervisor",
                    "project_start_date",
                )
            },
        ),
    )


@admin.register(Toolkit)
class ToolkitAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "github_url")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "description")


@admin.register(Studio)
class StudioAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "toolkit", "github_url")
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ("toolkit",)
    search_fields = ("name", "description")


@admin.register(Workflow)
class WorkflowAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "studio", "branch_name")
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ("studio", "studio__toolkit")
    search_fields = ("name", "description")


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "icon")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "description", "use_case")
