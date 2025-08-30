# Food Tracker Django Application

Food Tracker is a Django 5.0.3 web application for tracking food-related data. The project includes a basic "counter" app with a home page and uses SQLite for data storage. The application includes Django admin functionality and uses a Windows-style virtual environment.

Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

## Working Effectively

### Bootstrap and Setup
Run these commands to set up the development environment:

```bash
cd /path/to/food-tracker
# Set Python path to use the included virtual environment
export PYTHONPATH="/path/to/food-tracker/venv/Lib/site-packages"
```

**CRITICAL**: This project uses a Windows-style virtual environment with Django pre-installed. Always use the `PYTHONPATH` environment variable to access the Django installation.

### Database Setup
- Run initial migrations (takes ~1 second, NEVER CANCEL):
```bash
PYTHONPATH="/path/to/food-tracker/venv/Lib/site-packages" python3 manage.py migrate
```

### Run Development Server
- Start the Django development server:
```bash
PYTHONPATH="/path/to/food-tracker/venv/Lib/site-packages" python3 manage.py runserver 0.0.0.0:8000
```
- The server starts immediately (~1 second startup time)
- Access the application at: http://localhost:8000/ 
- Access admin interface at: http://localhost:8000/admin/

### Testing
- Run Django system check (takes ~0.25 seconds, NEVER CANCEL):
```bash
PYTHONPATH="/path/to/food-tracker/venv/Lib/site-packages" python3 manage.py check
```

- Run tests (takes ~0.30 seconds, NEVER CANCEL):
```bash
PYTHONPATH="/path/to/food-tracker/venv/Lib/site-packages" python3 manage.py test
```

**Note**: Currently no custom tests are implemented - this will show "NO TESTS RAN" which is expected.

### Admin Interface Setup
- Create a superuser for admin access:
```bash
PYTHONPATH="/path/to/food-tracker/venv/Lib/site-packages" python3 manage.py createsuperuser --username admin --email admin@example.com --noinput
```

- Set password programmatically:
```bash
echo "from django.contrib.auth.models import User; u=User.objects.get(username='admin'); u.set_password('admin123'); u.save()" | PYTHONPATH="/path/to/food-tracker/venv/Lib/site-packages" python3 manage.py shell
```

- Login credentials: username=`admin`, password=`admin123`

## Validation

### Manual Testing Scenarios
Always run through these validation steps after making changes:

1. **Basic Application Test**:
   - Start the development server
   - Navigate to http://localhost:8000/
   - Verify "Hello world" heading is displayed
   - Stop the server with Ctrl+C

2. **Admin Interface Test**:
   - Start the development server  
   - Navigate to http://localhost:8000/admin/
   - Login with admin/admin123 credentials
   - Verify admin dashboard loads with "Authentication and Authorization" section
   - Test basic navigation (Users, Groups links)

3. **Database Operations Test**:
   - Run system check: `python3 manage.py check`
   - Run migrations: `python3 manage.py migrate` 
   - Verify no errors in database operations

### Automated Validation
- Always run `python3 manage.py check` before committing changes
- Always run `python3 manage.py test` to verify no test regressions

## Project Structure

### Key Files and Directories
```
food-tracker/
├── manage.py              # Django management script
├── db.sqlite3            # SQLite database (created after migrations)
├── .gitignore            # Git ignore rules (includes Python cache files)
├── foodie/               # Main Django project directory
│   ├── settings.py       # Django configuration
│   ├── urls.py          # Root URL configuration
│   ├── wsgi.py          # WSGI application entry point
│   └── asgi.py          # ASGI application entry point
├── counter/              # Django app for main functionality
│   ├── models.py        # Data models (currently empty)
│   ├── views.py         # View functions (home view)
│   ├── urls.py          # App URL patterns
│   ├── admin.py         # Admin configuration
│   ├── tests.py         # Test cases (currently empty)
│   └── templates/       # HTML templates
│       └── home.html    # Home page template
└── venv/                # Virtual environment (Windows-style)
    ├── Scripts/         # Executables (django-admin.exe, pip.exe, python.exe)
    └── Lib/site-packages/  # Python packages including Django 5.0.3
```

### Important Notes
- **Virtual Environment**: Uses Windows-style structure with `Scripts/` and `Lib/` directories
- **Database**: Uses SQLite with file-based storage (`db.sqlite3`)
- **Static Files**: Django handles static file serving in development mode
- **Templates**: Simple HTML templates in `counter/templates/`

### Common Commands Reference
All commands must include the PYTHONPATH environment variable:

```bash
# System management
PYTHONPATH="/path/to/food-tracker/venv/Lib/site-packages" python3 manage.py check
PYTHONPATH="/path/to/food-tracker/venv/Lib/site-packages" python3 manage.py migrate
PYTHONPATH="/path/to/food-tracker/venv/Lib/site-packages" python3 manage.py runserver 0.0.0.0:8000

# Database operations
PYTHONPATH="/path/to/food-tracker/venv/Lib/site-packages" python3 manage.py makemigrations
PYTHONPATH="/path/to/food-tracker/venv/Lib/site-packages" python3 manage.py shell
PYTHONPATH="/path/to/food-tracker/venv/Lib/site-packages" python3 manage.py dbshell

# User management
PYTHONPATH="/path/to/food-tracker/venv/Lib/site-packages" python3 manage.py createsuperuser
PYTHONPATH="/path/to/food-tracker/venv/Lib/site-packages" python3 manage.py changepassword admin

# Testing
PYTHONPATH="/path/to/food-tracker/venv/Lib/site-packages" python3 manage.py test
```

## Troubleshooting

### Common Issues
1. **Django not found**: Ensure PYTHONPATH is set correctly to point to `venv/Lib/site-packages`
2. **Database errors**: Run `python3 manage.py migrate` to apply migrations
3. **Admin login fails**: Reset password using the shell command provided above
4. **Port already in use**: Use different port like `python3 manage.py runserver 0.0.0.0:8001`

### Performance Expectations
- Server startup: ~1 second
- System check: ~0.25 seconds  
- Test execution: ~0.30 seconds
- Database migrations: ~1-2 seconds

## Development Workflow

### Making Changes
1. Set environment variable: `export PYTHONPATH="/path/to/food-tracker/venv/Lib/site-packages"`
2. Run system check to verify current state
3. Make your changes to models, views, templates, or URLs
4. Test changes using the development server
5. Run system check again to verify no issues introduced
6. Run tests to ensure no regressions
7. Test admin interface if user-related changes were made

### Adding New Features
- **Models**: Add to `counter/models.py`, then run `makemigrations` and `migrate`
- **Views**: Add to `counter/views.py` and update `counter/urls.py`
- **Templates**: Add HTML files to `counter/templates/`
- **Admin**: Configure in `counter/admin.py` to manage models via admin interface

Always test new features through both direct URL access and admin interface where applicable.