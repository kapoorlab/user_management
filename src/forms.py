from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import LabUser


class CustomUserCreationForm(UserCreationForm):
    """Form for creating new lab users."""

    class Meta:
        model = LabUser
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "uni_email",
            "github_username",
            "basecamp_id",
            "supervisor",
            "project_start_date",
        )
        widgets = {
            "project_start_date": forms.DateInput(attrs={"type": "date"}),
        }


class CustomUserChangeForm(UserChangeForm):
    """Form for updating lab users."""

    class Meta:
        model = LabUser
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "uni_email",
            "github_username",
            "basecamp_id",
            "supervisor",
            "project_start_date",
        )
        widgets = {
            "project_start_date": forms.DateInput(attrs={"type": "date"}),
        }


class LabUserProfileForm(forms.ModelForm):
    """Form for users to update their own profile."""

    class Meta:
        model = LabUser
        fields = (
            "first_name",
            "last_name",
            "email",
            "uni_email",
            "github_username",
            "basecamp_id",
        )
