# alx_travel_app/settings.py
import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

# ─── 1) Base Directory & Environment Variables ────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")  # Load .env from project root

# Security settings
SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-prod")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# --- UPDATED SECTION ---
# This list allows your app to run locally on 127.0.0.1 and localhost.
ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
]

# This line gets the auto-generated domain name from Render when deployed.
RENDER_EXTERNAL_HOSTNAME = os.getenv('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
# --- END UPDATED SECTION ---


# Chapa payment settings
CHAPA_SECRET_KEY = os.getenv("CHAPA_SECRET_KEY", "")
FRONTEND_RETURN_URL = os.getenv("FRONTEND_RETURN_URL", "http://localhost:3000/payment/success")
API_CALLBACK_URL = os.getenv("API_CALLBACK_URL", "http://127.0.0.1:8000/api/payments/verify/")

# ─── 2) Installed Apps ────────────────────────────────────────────────────────
INSTALLED_APPS = [
    # Django core
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party
    "rest_framework",
    "corsheaders",
    "drf_yasg",
    "django_ip_geolocation",
    # Local apps
    "listings",
]

# ─── 3) Middleware ────────────────────────────────────────────────────────────
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_ip_geolocation.middleware.IpGeolocationMiddleware",
]

# ─── 4) URLs & WSGI/ASGI ──────────────────────────────────────────────────────
ROOT_URLCONF = "alx_travel_app.urls"
WSGI_APPLICATION = "alx_travel_app.wsgi.application"
ASGI_APPLICATION = "alx_travel_app.asgi.application"

# ─── 5) Templates ─────────────────────────────────────────────────────────────
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ─── 6) Database ──────────────────────────────────────────────────────────────
DATABASES = {
    "default": dj_database_url.config(
        default=os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'db.sqlite3'}"),
        conn_max_age=600
    )
}

# ─── 7) Authentication & Passwords ────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ─── 8) Internationalization & Time Zone ──────────────────────────────────────
LANGUAGE_CODE = "en-us"
TIME_ZONE = os.getenv("TIME_ZONE", "Africa/Lagos")
USE_I18N = True
USE_TZ = True

# ─── 9) Static & Media Files ──────────────────────────────────────────────────
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"] if (BASE_DIR / "static").exists() else []
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ─── 10) CORS & CSRF ──────────────────────────────────────────────────────────
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
] + ([os.getenv("FRONTEND_URL")] if os.getenv("FRONTEND_URL") else [])
CORS_ALLOW_ALL_ORIGINS = os.getenv("CORS_ALLOW_ALL", "False").lower() == "true"
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
] + ([os.getenv("API_CALLBACK_URL")] if os.getenv("API_CALLBACK_URL") else [])

# ─── 11) Django REST Framework ────────────────────────────────────────────────
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",
}

# ─── 12) Swagger (drf_yasg) ───────────────────────────────────────────────────
SWAGGER_SETTINGS = {
    "DOC_EXPANSION": "none",
    "USE_SESSION_AUTH": False,
    "JSON_EDITOR": True,
}

# ─── 13) Celery Configuration ─────────────────────────────────────────────────
CELERY_BROKER_URL = os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0")
CELERY_RESULT_BACKEND = os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = os.getenv("TIME_ZONE", "Africa/Lagos")

# ─── 14) Email Settings ───────────────────────────────────────────────────────
EMAIL_BACKEND = os.getenv("EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "no-reply@alxtravelapp.com")

# ─── 15) IP Geolocation (django-ip-geolocation) ───────────────────────────────
IP_GEOLOCATION_SETTINGS = {
    "BACKEND": "ipapi",
    "API_KEY": os.getenv("IPAPI_API_KEY", ""),
    "ENABLED": os.getenv("IP_GEOLOCATION_ENABLED", "True").lower() == "true",
}

# ─── 16) Logging ──────────────────────────────────────────────────────────────
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}