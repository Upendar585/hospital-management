# Hospital Management System

Django application for patient registration, doctor access, and appointment management.

## Local development

Set these variables in PowerShell, then run Django with your virtual environment active:

```powershell
$env:DJANGO_DEBUG = "True"
$env:DJANGO_SECRET_KEY = "local-development-only-secret"
$env:DJANGO_ALLOWED_HOSTS = "127.0.0.1,localhost"
python manage.py migrate
python manage.py runserver
```

## Railway deployment

1. Push this repository to GitHub.
2. In Railway, create a project from the GitHub repository and add a **MySQL** database service.
3. In the Django service's **Variables** tab, add the variables in `.env.example`. For every `MYSQL...` value, select the matching value from the MySQL service using Railway's variable-reference picker.
4. Replace `DJANGO_SECRET_KEY` with a unique random value and set `DJANGO_ALLOWED_HOSTS` to the Railway public domain.
5. Deploy the Django service, then generate a public domain under **Settings → Networking**.

`railway.json` collects static files, runs migrations, starts Gunicorn, and checks `/health/` before a release becomes available.

## Required production variables

```text
DJANGO_DEBUG=False
DJANGO_SECRET_KEY=<unique secret>
DJANGO_ALLOWED_HOSTS=<your-app>.up.railway.app
MYSQLHOST=<Railway MySQL host>
MYSQLPORT=<Railway MySQL port>
MYSQLUSER=<Railway MySQL user>
MYSQLPASSWORD=<Railway MySQL password>
MYSQLDATABASE=<Railway MySQL database>
```

Set `MYSQL_SSL_CA` only when your database provider supplies a CA certificate path and requires TLS. Railway's private service network does not require a public database endpoint.
