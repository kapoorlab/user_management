# Building a Django User Management App - Step by Step Tutorial

This tutorial walks you through creating a Django app with custom user management and project tracking from scratch.

## Prerequisites

- Python 3.8+
- pip

## Step 1: Create Virtual Environment and Install Django

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Django
pip install django
```

## Step 2: Create Django Project and App

```bash
# Create project
django-admin startproject myproject
cd myproject

# Create app
python manage.py startapp user_management
```

## Step 3: Configure Settings

Edit `myproject/settings.py`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'user_management',  # Add your app
]

# Set custom user model (MUST be done before first migration)
AUTH_USER_MODEL = 'user_management.LabUser'

# Login/Logout redirects
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'dashboard'
```

## Step 4: Create Custom User Model

Edit `user_management/models.py`:

```python
from django.db import models
from django.contrib.auth.models import AbstractUser


class LabUser(AbstractUser):
    """Custom user model with additional fields."""
    uni_email = models.EmailField(
        blank=True,
        help_text="University email address"
    )
    github_username = models.CharField(
        max_length=100,
        blank=True,
        help_text="GitHub username"
    )
    basecamp_id = models.CharField(
        max_length=100,
        blank=True,
        help_text="Basecamp user ID"
    )
    supervisor = models.CharField(
        max_length=200,
        blank=True,
        help_text="Name of supervisor"
    )
    project_start_date = models.DateField(
        null=True,
        blank=True,
        help_text="Start date of project/position"
    )

    class Meta:
        ordering = ['username']

    def __str__(self):
        return f"{self.username} ({self.get_full_name() or 'No name'})"
```

## Step 5: Create Custom User Forms

Create `user_management/forms.py`:

```python
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import LabUser


class CustomUserCreationForm(UserCreationForm):
    """Form for creating new users."""

    class Meta:
        model = LabUser
        fields = (
            'username', 'email', 'first_name', 'last_name',
            'uni_email', 'github_username', 'basecamp_id',
            'supervisor', 'project_start_date'
        )
        widgets = {
            'project_start_date': forms.DateInput(attrs={'type': 'date'}),
        }


class CustomUserChangeForm(UserChangeForm):
    """Form for updating users."""

    class Meta:
        model = LabUser
        fields = (
            'username', 'email', 'first_name', 'last_name',
            'uni_email', 'github_username', 'basecamp_id',
            'supervisor', 'project_start_date'
        )
        widgets = {
            'project_start_date': forms.DateInput(attrs={'type': 'date'}),
        }
```

## Step 6: Register Models in Admin

Edit `user_management/admin.py`:

```python
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import LabUser
from .forms import CustomUserCreationForm, CustomUserChangeForm


@admin.register(LabUser)
class LabUserAdmin(UserAdmin):
    """Admin for custom LabUser model."""
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = LabUser
    list_display = ('username', 'email', 'uni_email', 'supervisor', 'is_staff')
    list_filter = ('is_staff', 'is_active', 'supervisor')
    search_fields = ('username', 'email', 'uni_email')
    ordering = ('username',)

    fieldsets = UserAdmin.fieldsets + (
        ('Lab Info', {
            'fields': ('uni_email', 'github_username', 'basecamp_id',
                      'supervisor', 'project_start_date')
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Lab Info', {
            'fields': ('uni_email', 'github_username', 'basecamp_id',
                      'supervisor', 'project_start_date')
        }),
    )
```

## Step 7: Create Views

Edit `user_management/views.py`:

```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import CustomUserCreationForm


def dashboard(request):
    """Main dashboard."""
    return render(request, 'user_management/dashboard.html')


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
            return render(request, "registration/register.html", {"form": form})


@login_required
def profile(request):
    """User profile view."""
    return render(request, 'user_management/profile.html', {'user': request.user})
```

## Step 8: Configure URLs

Create `user_management/urls.py`:

```python
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
]
```

Update `myproject/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('user_management.urls')),
]
```

## Step 9: Create Templates

Create directory structure:
```
user_management/
    templates/
        user_management/
            base.html
            dashboard.html
            profile.html
        registration/
            login.html
            register.html
```

**base.html:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}My App{% endblock %}</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-4">
        <div class="container">
            <a class="navbar-brand" href="{% url 'dashboard' %}">My App</a>
            <ul class="navbar-nav ms-auto">
                {% if user.is_authenticated %}
                    <li class="nav-item"><a class="nav-link" href="{% url 'profile' %}">{{ user.username }}</a></li>
                    <li class="nav-item"><a class="nav-link" href="{% url 'logout' %}">Logout</a></li>
                {% else %}
                    <li class="nav-item"><a class="nav-link" href="{% url 'login' %}">Login</a></li>
                    <li class="nav-item"><a class="nav-link" href="{% url 'register' %}">Register</a></li>
                {% endif %}
            </ul>
        </div>
    </nav>
    <div class="container">
        {% block content %}{% endblock %}
    </div>
</body>
</html>
```

**login.html:**
```html
{% extends 'user_management/base.html' %}
{% block title %}Login{% endblock %}
{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6">
        <h2>Login</h2>
        <form method="post">
            {% csrf_token %}
            {{ form.as_p }}
            <button type="submit" class="btn btn-primary">Login</button>
        </form>
        <p class="mt-3">Don't have an account? <a href="{% url 'register' %}">Register</a></p>
    </div>
</div>
{% endblock %}
```

**register.html:**
```html
{% extends 'user_management/base.html' %}
{% block title %}Register{% endblock %}
{% block content %}
<div class="row justify-content-center">
    <div class="col-md-8">
        <h2>Register</h2>
        <form method="post">
            {% csrf_token %}
            {{ form.as_p }}
            <button type="submit" class="btn btn-primary">Register</button>
        </form>
        <p class="mt-3">Already have an account? <a href="{% url 'login' %}">Login</a></p>
    </div>
</div>
{% endblock %}
```

## Step 10: Create and Apply Migrations

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

## Step 11: Run Development Server

```bash
python manage.py runserver
```

Visit:
- http://127.0.0.1:8000/ - Dashboard
- http://127.0.0.1:8000/admin/ - Admin interface
- http://127.0.0.1:8000/register/ - Registration
- http://127.0.0.1:8000/accounts/login/ - Login

## Adding More Models

To add project/toolkit models like in this app, add them to `models.py`:

```python
class Project(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    owner = models.ForeignKey(LabUser, on_delete=models.CASCADE, related_name='projects')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
```

Remember to:
1. Register in `admin.py`
2. Create views in `views.py`
3. Add URLs in `urls.py`
4. Create templates
5. Run `makemigrations` and `migrate`

## Key Concepts

- **AbstractUser**: Extends Django's built-in User model with custom fields
- **AUTH_USER_MODEL**: Must be set before first migration
- **UserAdmin**: Provides admin interface for user management
- **login_required**: Decorator to protect views
- **get_object_or_404**: Safe object retrieval with 404 on missing

## Common Issues

1. **"AUTH_USER_MODEL refers to model that has not been installed"**
   - Ensure app is in INSTALLED_APPS
   - Set AUTH_USER_MODEL before any migrations

2. **Migration errors with custom user**
   - Delete all migrations and database
   - Set AUTH_USER_MODEL first
   - Run fresh migrations

3. **Template not found**
   - Check directory structure matches app name
   - Ensure 'APP_DIRS': True in TEMPLATES settings

---

## Production Deployment with Nginx

This section covers deploying your Django app behind Nginx with SSL and basic authentication.

### Step 1: Install Nginx (macOS)

```bash
brew install nginx
```

Nginx config location: `/opt/homebrew/etc/nginx/` (Apple Silicon) or `/usr/local/etc/nginx/` (Intel)

### Step 2: Generate SSL Certificates

For local/internal use, create self-signed certificates using [mkcert](https://github.com/FiloSottile/mkcert):

```bash
brew install mkcert
mkcert -install
mkcert 131.173.36.128  # Replace with your IP
```

This creates `131.173.36.128.pem` and `131.173.36.128-key.pem` in the current directory.

Move them to a secure location:
```bash
mv 131.173.36.128*.pem ~/
```

### Step 3: Create Password File for Basic Auth

```bash
# Install htpasswd (comes with httpd)
brew install httpd

# Create password file
htpasswd -c /opt/homebrew/etc/nginx/.usermanagement-auth admin
```

Add more users:
```bash
htpasswd /opt/homebrew/etc/nginx/.usermanagement-auth newuser
```

### Step 4: Configure Django Settings

Update `config/settings.py` for running behind a reverse proxy:

```python
# Allowed hosts
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "131.173.36.128"]

# Static files - include the URL prefix
STATIC_URL = "/usermanagement/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# For running behind nginx at /usermanagement
FORCE_SCRIPT_NAME = "/usermanagement"
USE_X_FORWARDED_HOST = True
CSRF_TRUSTED_ORIGINS = ["https://131.173.36.128"]
```

### Step 5: Collect Static Files

```bash
python manage.py collectstatic
```

### Step 6: Configure Nginx

Edit `/opt/homebrew/etc/nginx/nginx.conf`:

```nginx
worker_processes  1;

events {
    worker_connections  1024;
}

http {
    include       mime.types;
    default_type  application/octet-stream;
    sendfile        on;
    keepalive_timeout  65;

    server {
        listen 443 ssl;
        server_name 131.173.36.128;

        ssl_certificate     /Users/youruser/131.173.36.128.pem;
        ssl_certificate_key /Users/youruser/131.173.36.128-key.pem;

        # Django User Management App
        location /usermanagement/ {
            proxy_pass http://127.0.0.1:8000/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_set_header X-Script-Name /usermanagement;

            # Basic authentication
            auth_basic "Restricted Access";
            auth_basic_user_file /opt/homebrew/etc/nginx/.usermanagement-auth;
        }

        # Serve static files directly
        location /usermanagement/static/ {
            alias /path/to/your/project/staticfiles/;
        }
    }
}
```

### Step 7: Test and Start Nginx

```bash
# Test configuration
nginx -t

# Start nginx
brew services start nginx

# Or reload if already running
nginx -s reload
```

### Step 8: Run Django

```bash
python manage.py runserver 127.0.0.1:8000
```

### Step 9: Access Your App

Visit: `https://131.173.36.128/usermanagement/`

You'll be prompted for the username/password you created with htpasswd.

Admin interface: `https://131.173.36.128/usermanagement/admin/`

### Nginx Commands Reference

```bash
# Start nginx
brew services start nginx

# Stop nginx
brew services stop nginx

# Restart nginx
brew services restart nginx

# Reload config without restart
nginx -s reload

# Test configuration
nginx -t

# View error logs
tail -f /opt/homebrew/var/log/nginx/error.log
```

### Running Django as a Background Service

For production, use Gunicorn instead of the development server:

```bash
pip install gunicorn

# Run with gunicorn
gunicorn config.wsgi:application --bind 127.0.0.1:8000

# Run in background with nohup
nohup gunicorn config.wsgi:application --bind 127.0.0.1:8000 &
```

### Adding Multiple Apps to Nginx

You can serve multiple Django apps on different paths:

```nginx
server {
    listen 443 ssl;
    server_name 131.173.36.128;

    ssl_certificate     /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    # App 1: User Management
    location /usermanagement/ {
        proxy_pass http://127.0.0.1:8000/;
        auth_basic "User Management";
        auth_basic_user_file /opt/homebrew/etc/nginx/.usermanagement-auth;
        # ... other proxy headers
    }

    # App 2: Another Django App
    location /otherapp/ {
        proxy_pass http://127.0.0.1:8001/;
        auth_basic "Other App";
        auth_basic_user_file /opt/homebrew/etc/nginx/.otherapp-auth;
        # ... other proxy headers
    }

    # App 3: Streamlit or other service
    location / {
        proxy_pass http://127.0.0.1:8501/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        # ... other proxy headers
    }
}
```

### Security Notes

1. **Never expose Django's development server directly** - Always use Nginx as a reverse proxy
2. **Use strong passwords** for htpasswd authentication
3. **Keep SSL certificates secure** - Restrict file permissions
4. **In production**, use proper SSL certificates from Let's Encrypt or a CA
5. **Set DEBUG=False** in production settings
