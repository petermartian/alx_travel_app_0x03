import os
from pathlib import Path
from dotenv import load_dotenv

# ─── 1. BASE DIR & ENV SETUP ─────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(BASE_DIR, '.env'))

CHAPA_SECRET_KEY = os.getenv('CHAPA_SECRET_KEY', '')
FRONTEND_RETURN_URL = os.getenv('FRONTEND_RETURN_URL', 'http://localhost:3000/payment/success')
API_CALLBACK_URL = os.getenv('API_CALLBACK_URL', 'http://localhost:8000/api/payment/verify/')

# Dev email backend (prints to console)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'no-reply@example.com'

# ─── 2. SECURITY ────────────────────────────────────────────────────
SECRET_KEY = os.getenv('SECRET_KEY', 'your-default-secret-key-for-dev-only-change-this')
DEBUG = os.getenv('DEBUG', 'True') == 'True'  # Convert string to boolean
ALLOWED_HOSTS = ['localhost', '127.0.0.1']  # Tighten in production

# ─── 3. INSTALLED APPS ──────────────────────────────────────────────
INSTALLED_APPS = [
    # Django default apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
    'rest_framework',
    'corsheaders',
    'drf_yasg',

    # Your apps
    'listings',
]

# ─── 4. MIDDLEWARE ───────────────────────────────────────────────────
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Must be first for CORS
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'alx_travel_app.urls'

# ─── 5. TEMPLATES & WSGI ────────────────────────────────────────────
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'alx_travel_app.wsgi.application'

# ─── 6. DATABASE (MySQL) ────────────────────────────────────────────
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# ─── 7. PASSWORD VALIDATION ─────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# ─── 8. INTERNATIONALIZATION & STATIC FILES ─────────────────────────
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ─── 9. CORS SETTINGS ───────────────────────────────────────────────
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
]
CORS_ALLOW_ALL_ORIGINS = False  # Secure for dev, update for production

# ─── 10. REST FRAMEWORK ─────────────────────────────────────────────
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
}

# ─── 11. SWAGGER / drf-yasg ──────────────────────────────────────────
SWAGGER_SETTINGS = {
    'DOC_EXPANSION': 'none',
    'USE_SESSION_AUTH': False,
    'JSON_EDITOR': True,
}

# ─── 12. EMAIL / CELERY ──────────────────────────────────────────────
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'