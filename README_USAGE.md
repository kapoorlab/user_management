# NeuroAI Lab User Management - Usage Guide

This guide explains how to set up, launch, and manage the NeuroAI Lab user management application.

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <repository-url>
cd user_management

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install django
```

### 2. Project Setup

Create a Django project that uses this app:

```bash
# Create new project (if not exists)
django-admin startproject neuroai_project
cd neuroai_project

# Copy/link the user_management app into the project
cp -r ../user_management/src ./user_management
```

### 3. Configure Settings

Edit `neuroai_project/settings.py`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'user_management',
]

# CRITICAL: Set custom user model BEFORE first migration
AUTH_USER_MODEL = 'user_management.LabUser'

# Redirect settings
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'dashboard'
```

Update `neuroai_project/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('user_management.urls')),
]
```

### 4. Initialize Database

```bash
# Create migrations for new models
python manage.py makemigrations user_management

# Apply all migrations
python manage.py migrate

# Create admin superuser
python manage.py createsuperuser
```

### 5. Launch the Server

```bash
# Development server
python manage.py runserver

# Or specify port
python manage.py runserver 8080

# Or bind to all interfaces (for remote access)
python manage.py runserver 0.0.0.0:8000
```

## User Fields

Each LabUser has the following fields:

| Field | Description | Required |
|-------|-------------|----------|
| `username` | Login username | Yes |
| `password` | Login password | Yes |
| `email` | General email address | No |
| `first_name` | First name | No |
| `last_name` | Last name | No |
| `uni_email` | University of Osnabrueck email | No |
| `github_username` | GitHub username | No |
| `basecamp_id` | Basecamp user ID | No |
| `supervisor` | Name of supervisor | No |
| `project_start_date` | Start date of project | No |

## Managing Users

### Via Admin Interface

1. Go to http://127.0.0.1:8000/admin/
2. Login with superuser credentials
3. Click "Lab users" under "USER_MANAGEMENT"

#### Create User
1. Click "Add Lab User" button
2. Fill in username and password
3. Click "Save and continue editing"
4. Fill in additional fields (Lab Info section)
5. Click "Save"

#### Edit User
1. Click on username in user list
2. Modify fields as needed
3. Click "Save"

#### Delete User
1. Select user(s) with checkbox
2. Select "Delete selected lab users" from Action dropdown
3. Click "Go"
4. Confirm deletion

#### Change Password
1. Click on username
2. Click "this form" link next to password field
3. Enter new password twice
4. Click "Change password"

### Via Command Line

```bash
# Create superuser (admin)
python manage.py createsuperuser

# Create regular user via shell
python manage.py shell
```

```python
from user_management.models import LabUser
from datetime import date

# Create user
user = LabUser.objects.create_user(
    username='jdoe',
    email='jdoe@example.com',
    password='securepassword123',
    first_name='John',
    last_name='Doe',
    uni_email='jdoe@uni-osnabrueck.de',
    github_username='johndoe',
    basecamp_id='12345',
    supervisor='Prof. Smith',
    project_start_date=date(2024, 1, 15)
)

# Update user
user.supervisor = 'Prof. Jones'
user.save()

# Delete user
user.delete()

# List all users
for u in LabUser.objects.all():
    print(f"{u.username}: {u.uni_email} - Supervisor: {u.supervisor}")

# Find users by supervisor
LabUser.objects.filter(supervisor='Prof. Smith')

# Find users who started in 2024
LabUser.objects.filter(project_start_date__year=2024)
```

### Via Management Command (Optional)

Create `user_management/management/commands/create_lab_user.py`:

```python
from django.core.management.base import BaseCommand
from user_management.models import LabUser
from datetime import datetime

class Command(BaseCommand):
    help = 'Create a new lab user'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('--uni-email', type=str)
        parser.add_argument('--github', type=str)
        parser.add_argument('--supervisor', type=str)
        parser.add_argument('--start-date', type=str, help='YYYY-MM-DD')

    def handle(self, *args, **options):
        start_date = None
        if options['start_date']:
            start_date = datetime.strptime(options['start_date'], '%Y-%m-%d').date()

        user = LabUser.objects.create_user(
            username=options['username'],
            email=options['email'],
            uni_email=options.get('uni_email', ''),
            github_username=options.get('github', ''),
            supervisor=options.get('supervisor', ''),
            project_start_date=start_date,
        )
        self.stdout.write(f'Created user: {user.username}')
```

Usage:
```bash
python manage.py create_lab_user jdoe jdoe@email.com \
    --uni-email jdoe@uni-osnabrueck.de \
    --github johndoe \
    --supervisor "Prof. Smith" \
    --start-date 2024-01-15
```

## URL Endpoints

| URL | Description |
|-----|-------------|
| `/` | Dashboard |
| `/admin/` | Admin interface |
| `/accounts/login/` | Login page |
| `/accounts/logout/` | Logout |
| `/accounts/password_change/` | Change password |
| `/accounts/password_reset/` | Reset password |
| `/register/` | New user registration |
| `/toolkits/` | List all toolkits |
| `/toolkit/<slug>/` | Toolkit details |
| `/studios/` | List all studios |
| `/studio/<slug>/` | Studio details |
| `/datasets/` | List all datasets |
| `/dataset/<slug>/` | Dataset details |

## Managing Toolkits, Studios, and Workflows

### Via Admin

1. Go to http://127.0.0.1:8000/admin/
2. Click on "Toolkits", "Studios", "Workflows", or "Datasets"
3. Add/Edit/Delete as needed

### Via Shell

```python
from user_management.models import Toolkit, Studio, Workflow, Dataset

# Create toolkit
toolkit = Toolkit.objects.create(
    name='Lightning Kietzmannlab',
    slug='lightning-kietzmannlab',
    description='Core deep learning framework',
    github_url='https://github.com/kietzmannlab/lightning-kietzmannlab',
    icon='⚡',
    color='#43e97b',
    modules='lightning_simclr_model\nlightning_trainer\npytorch_models'
)

# Create studio
studio = Studio.objects.create(
    name='Lightning Kietzmannlab Studio',
    slug='lightning-kietzmannlab-studio',
    description='Training workflows and experiments',
    toolkit=toolkit,
    github_url='https://github.com/kietzmannlab/lightning-kietzmannlab-studio',
    icon='🔬'
)

# Create workflow
workflow = Workflow.objects.create(
    name='SimCLR Training',
    slug='simclr',
    description='Self-supervised contrastive learning',
    studio=studio,
    branch_name='simclr-training',
    datasets='ImageNet\nCIFAR-10'
)
```

## Backup and Restore

### Backup Database

```bash
# SQLite (default)
cp db.sqlite3 db.sqlite3.backup

# Export data as JSON
python manage.py dumpdata user_management > backup.json

# Export only users
python manage.py dumpdata user_management.labuser > users.json
```

### Restore Database

```bash
# From JSON backup
python manage.py loaddata backup.json
```

## Production Deployment

### Environment Variables

```bash
export DJANGO_SECRET_KEY='your-secret-key-here'
export DJANGO_DEBUG='False'
export DJANGO_ALLOWED_HOSTS='yourdomain.com,www.yourdomain.com'
```

### Static Files

```bash
python manage.py collectstatic
```

### Using Gunicorn

```bash
pip install gunicorn
gunicorn neuroai_project.wsgi:application --bind 0.0.0.0:8000
```

### Using with Nginx

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location /static/ {
        alias /path/to/staticfiles/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Troubleshooting

### "No such table" error
```bash
python manage.py migrate
```

### "AUTH_USER_MODEL refers to model that has not been installed"
- Ensure `user_management` is in `INSTALLED_APPS`
- Ensure `AUTH_USER_MODEL = 'user_management.LabUser'` is set

### Migration conflicts
```bash
# Reset migrations (development only!)
rm -rf user_management/migrations/
python manage.py makemigrations user_management
python manage.py migrate --fake-initial
```

### Cannot login to admin
```bash
python manage.py createsuperuser
```

### Static files not loading
```bash
python manage.py collectstatic
# Ensure STATIC_URL and STATIC_ROOT are configured
```
