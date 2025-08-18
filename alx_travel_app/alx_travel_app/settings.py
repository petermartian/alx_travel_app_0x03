# alx_travel_app/settings.py
import os
from pathlib import Path
from dotenv import load_dotenv

# ─── 1) BASE DIR & ENV ──────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")  # Loads .env at project root

# Secrets / keys
SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-prod")
DEBUG = os.getenv("DEBUG", "True").lower() == "true"
ALLOWED_HOSTS = [h.strip() for h in os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",") if h.strip()]

# Chapa envs
CHAPA_SECRET_KEY = os.getenv("CHAPA_SECRET_KEY", "")
FRONTEND_RETURN_URL = os.getenv("FRONTEND_RETURN_URL", "http://localhost:3000/payment/success")
API_CALLBACK_URL = os.getenv("API_CALLBACK_URL", "http://127.0.0.1:8000/api/payments/verify/")

# Email (console for dev)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "no-reply@example.com")

# ─── 2) APPS ───────────────────────────────────────────────────────────────────
INSTALLED_APPS = [
    # Django
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

    # Local apps
    "listings",
]

# ─── 3) MIDDLEWARE ─────────────────────────────────────────────────────────────
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # keep first
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "alx_travel_app.urls"

# ─── 4) TEMPLATES ──────────────────────────────────────────────────────────────
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

WSGI_APPLICATION = "alx_travel_app.wsgi.application"
ASGI_APPLICATION = "alx_travel_app.asgi.application"

# ─── 5) DATABASE ───────────────────────────────────────────────────────────────
# For smooth dev on macOS, default to SQLite. Switch to MySQL by uncommenting the MySQL block.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# # MySQL (optional)
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.mysql",
#         "NAME": os.getenv("DB_NAME", "alx_travel_db"),
#         "USER": os.getenv("DB_USER", "root"),
#         "PASSWORD": os.getenv("DB_PASSWORD", ""),
#         "HOST": os.getenv("DB_HOST", "127.0.0.1"),
#         "PORT": os.getenv("DB_PORT", "3306"),
#         "OPTIONS": {"init_command": "SET sql_mode='STRICT_TRANS_TABLES'"},
#     }
# }

# ─── 6) AUTH / PASSWORDS ───────────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ─── 7) I18N / TZ ──────────────────────────────────────────────────────────────
LANGUAGE_CODE = "en-us"
TIME_ZONE = os.getenv("TIME_ZONE", "Africa/Lagos")
USE_I18N = True
USE_TZ = True

# ─── 8) STATIC / MEDIA ─────────────────────────────────────────────────────────
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"] if (BASE_DIR / "static").exists() else []

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ─── 9) CORS ───────────────────────────────────────────────────────────────────
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
CORS_ALLOW_ALL_ORIGINS = os.getenv("CORS_ALLOW_ALL", "False").lower() == "true"
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

# ─── 10) DRF ───────────────────────────────────────────────────────────────────
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    # You can plug in authentication classes later if needed
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",
}

# ─── 11) Swagger (drf_yasg) ────────────────────────────────────────────────────
SWAGGER_SETTINGS = {
    "DOC_EXPANSION": "none",
    "USE_SESSION_AUTH": False,
    "JSON_EDITOR": True,
}

# ─── 12) Celery (optional; safe to keep) ───────────────────────────────────────
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://127.0.0.1:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://127.0.0.1:6379/0")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"

# ─── 13) Logging (dev-friendly) ────────────────────────────────────────────────
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "INFO"},
}
