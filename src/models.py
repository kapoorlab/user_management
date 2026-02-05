from django.contrib.auth.models import AbstractUser
from django.db import models


class LabUser(AbstractUser):
    """Custom user model for NeuroAI Lab members."""

    uni_email = models.EmailField(
        blank=True,
        help_text="University of Osnabrueck email (e.g., user@uni-osnabrueck.de)",
    )
    github_username = models.CharField(
        max_length=100, blank=True, help_text="GitHub username"
    )
    basecamp_id = models.CharField(
        max_length=100, blank=True, help_text="Basecamp user ID"
    )
    supervisor = models.CharField(
        max_length=200, blank=True, help_text="Name of supervisor"
    )
    project_start_date = models.DateField(
        null=True, blank=True, help_text="Start date of project/position"
    )

    class Meta:
        ordering = ["username"]

    def __str__(self):
        return f"{self.username} ({self.get_full_name() or 'No name'})"


class Toolkit(models.Model):
    """Base packages/bricks - the foundational libraries."""

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    github_url = models.URLField(blank=True)
    icon = models.CharField(max_length=10, default="")  # emoji
    color = models.CharField(max_length=20, default="#43e97b")  # hex color
    modules = models.TextField(
        blank=True, help_text="Key modules, one per line"
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_modules_list(self):
        """Return modules as a list."""
        if self.modules:
            return [m.strip() for m in self.modules.split("\n") if m.strip()]
        return []


class Studio(models.Model):
    """Studios that use toolkits - workflow implementations."""

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    toolkit = models.ForeignKey(
        Toolkit, on_delete=models.CASCADE, related_name="studios"
    )
    github_url = models.URLField(blank=True)
    icon = models.CharField(max_length=10, default="")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Workflow(models.Model):
    """Branches/workflows within studios - specific tasks/experiments."""

    name = models.CharField(max_length=200)
    slug = models.SlugField()
    description = models.TextField()
    studio = models.ForeignKey(
        Studio, on_delete=models.CASCADE, related_name="workflows"
    )
    branch_name = models.CharField(
        max_length=100, blank=True, help_text="Git branch name"
    )
    datasets = models.TextField(
        blank=True, help_text="Datasets used, one per line"
    )

    class Meta:
        ordering = ["name"]
        unique_together = ["studio", "slug"]

    def __str__(self):
        return f"{self.studio.name} / {self.name}"

    def get_datasets_list(self):
        """Return datasets as a list."""
        if self.datasets:
            return [d.strip() for d in self.datasets.split("\n") if d.strip()]
        return []


class Dataset(models.Model):
    """Dataset classes available in the framework."""

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    icon = models.CharField(max_length=10, default="")
    use_case = models.TextField(blank=True)
    features = models.TextField(blank=True, help_text="Features, one per line")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_features_list(self):
        """Return features as a list."""
        if self.features:
            return [f.strip() for f in self.features.split("\n") if f.strip()]
        return []
