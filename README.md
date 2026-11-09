# Coderr Backend

REST API backend for the Coderr platform, built with Django and
Django REST Framework. The frontend is not part of this repository.

## Requirements

- Python 3.12 or higher
- pip
- Git

## Installation

1. Clone the repository:

   ```bash
   git clone <your-repository-url>
   cd coderr
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv

   # Windows (PowerShell)
   .venv\Scripts\Activate.ps1

   # macOS / Linux
   source .venv/bin/activate
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Apply the database migrations:

   ```bash
   python manage.py migrate
   ```

5. (Optional) Create an admin user:

   ```bash
   python manage.py createsuperuser
   ```

6. Start the development server:

   ```bash
   python manage.py runserver
   ```

The API is now available at `http://127.0.0.1:8000/api/`.
The admin interface is available at `http://127.0.0.1:8000/admin/`.

## Running the tests

```bash
coverage run manage.py test
coverage report
```

The project requires a test coverage of at least 95%.

## Project structure

```
coderr/
├── core/          # Project settings, main URL routing
├── auth_app/      # Registration and login
│   └── api/       # serializers, views, urls, permissions
├── manage.py
└── requirements.txt
```

Every app contains an `api/` folder with its serializers, views,
URLs and permissions.

## Notes

- Authentication is token based (`Authorization: Token <token>`).
- All endpoints require authentication by default. Public endpoints
  (e.g. registration and login) are explicitly opened with `AllowAny`.
- CORS is configured for the local frontend on port 5500
  (`CORS_ALLOWED_ORIGINS` in `core/settings.py`).
- The SQLite database is not part of the repository. It is created
  locally by running the migrations.