from django.contrib.auth import login
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import CustomUserCreationForm
from .models import Dataset, Studio, Toolkit, Workflow


def dashboard(request):
    """Main dashboard showing all toolkits."""
    toolkits = Toolkit.objects.prefetch_related("studios").all()
    return render(request, "projects/dashboard.html", {"toolkits": toolkits})


def toolkit_list(request):
    """List all toolkits."""
    toolkits = Toolkit.objects.prefetch_related("studios").all()
    return render(
        request, "projects/toolkit_list.html", {"toolkits": toolkits}
    )


def toolkit_detail(request, slug):
    """Show toolkit details with its studios."""
    toolkit = get_object_or_404(Toolkit, slug=slug)
    return render(
        request, "projects/toolkit_detail.html", {"toolkit": toolkit}
    )


def studio_list(request):
    """List all studios."""
    studios = (
        Studio.objects.select_related("toolkit")
        .prefetch_related("workflows")
        .all()
    )
    return render(request, "projects/studio_list.html", {"studios": studios})


def studio_detail(request, slug):
    """Show studio details with its workflows."""
    studio = get_object_or_404(
        Studio.objects.select_related("toolkit"), slug=slug
    )
    return render(request, "projects/studio_detail.html", {"studio": studio})


def workflow_detail(request, studio_slug, workflow_slug):
    """Show workflow details."""
    studio = get_object_or_404(Studio, slug=studio_slug)
    workflow = get_object_or_404(Workflow, studio=studio, slug=workflow_slug)
    return render(
        request,
        "projects/workflow_detail.html",
        {"workflow": workflow, "studio": studio},
    )


def dataset_list(request):
    """List all available datasets."""
    datasets = Dataset.objects.all()
    return render(
        request, "projects/dataset_list.html", {"datasets": datasets}
    )


def dataset_detail(request, slug):
    """Show dataset details."""
    dataset = get_object_or_404(Dataset, slug=slug)
    return render(
        request, "projects/dataset_detail.html", {"dataset": dataset}
    )


def register(request):
    """User registration view."""
    if request.method == "GET":
        form = CustomUserCreationForm()
        return render(request, "registration/register.html", {"form": form})
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse("dashboard"))
        else:
            return render(
                request, "registration/register.html", {"form": form}
            )
