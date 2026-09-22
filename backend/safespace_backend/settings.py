"""
SafeSpace Django settings.

Environment-controlled for both local development and production.
Production is governed by environment variables — no secrets in source code.
"""

from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Base directory
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# Load local .env for development (silently ignored in production if absent)
load_dotenv(BASE_DIR / ".env")

# ---------------------------------------------------------------------------
# Security
# ---------------------------------------------------------------------------
SECRET_KEY = os.environ["SECRET_KEY"]  # Hard fail — must be set

# DEBUG: safe default is False. Set DEBUG=True in local .env only.
DEBUG = os.getenv("DEBUG", "False") == "True"

# ALLOWED_HOSTS: comma-separated list. Defaults to localhost for dev.
# Production must set e.g. ALLOWED_HOSTS=safespace.yourdomain.com
ALLOWED_HOSTS = [
    h.strip()
    for h in os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")
    if h.strip()
]

# ---------------------------------------------------------------------------
# HTTPS / Cookie security
# Enabled only when HTTPS=True is set (production).
# Never enabled locally — avoids breaking dev without HTTPS.
# ---------------------------------------------------------------------------
_HTTPS = os.getenv("HTTPS", "False") == "True"

SECURE_SSL_REDIRECT          = _HTTPS
SESSION_COOKIE_SECURE        = _HTTPS
CSRF_COOKIE_SECURE           = _HTTPS
SECURE_HSTS_SECONDS          = 31536000 if _HTTPS else 0   # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = _HTTPS
SECURE_HSTS_PRELOAD          = _HTTPS
SECURE_BROWSER_XSS_FILTER   = True
SECURE_CONTENT_TYPE_NOSNIFF  = True
X_FRAME_OPTIONS              = "DENY"

# ---------------------------------------------------------------------------
# Application definition
# ---------------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party
    "corsheaders",
    "rest_framework",
    # Local
    "core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",   # static files (production)
    "corsheaders.middleware.CorsMiddleware",        # must be before CommonMiddleware
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "safespace_backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "safespace_backend.wsgi.application"

# ---------------------------------------------------------------------------
# Database
# Priority: DATABASE_URL env var (Railway/Heroku style) → individual vars → defaults
# ---------------------------------------------------------------------------
_DATABASE_URL = os.getenv("DATABASE_URL", "")

if _DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.parse(
            _DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("DB_NAME", "safespace"),
            "USER": os.getenv("DB_USER", "postgres"),
            "PASSWORD": os.getenv("DB_PASSWORD", ""),
            "HOST": os.getenv("DB_HOST", "localhost"),
            "PORT": os.getenv("DB_PORT", "5432"),
        }
    }

# ---------------------------------------------------------------------------
# Password validation
# ---------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ---------------------------------------------------------------------------
# Internationalisation
# ---------------------------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Africa/Nairobi"
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------------------------
# Static files — WhiteNoise for production serving
# ---------------------------------------------------------------------------
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ---------------------------------------------------------------------------
# Default primary key field type
# ---------------------------------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---------------------------------------------------------------------------
# Django REST Framework
# ---------------------------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
    ],
}

# ---------------------------------------------------------------------------
# Email — console for dev, dummy for production (SafeSpace sends no email)
# ---------------------------------------------------------------------------
if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
else:
    EMAIL_BACKEND = "django.core.mail.backends.dummy.EmailBackend"

# ---------------------------------------------------------------------------
# CORS — restricted, never wildcard
# Production must set CORS_ALLOWED_ORIGINS to the actual frontend domain.
# ---------------------------------------------------------------------------
CORS_ALLOWED_ORIGINS = [
    o.strip()
    for o in os.getenv(
        "CORS_ALLOWED_ORIGINS",
        "http://localhost:3000,http://127.0.0.1:3000",
    ).split(",")
    if o.strip()
]
CORS_ALLOW_CREDENTIALS = False  # SafeSpace uses no cookies or auth tokens

# ---------------------------------------------------------------------------
# CSRF trusted origins (required when frontend is on a different domain)
# Production must set this to the actual frontend origin(s).
# ---------------------------------------------------------------------------
CSRF_TRUSTED_ORIGINS = [
    o.strip()
    for o in os.getenv(
        "CSRF_TRUSTED_ORIGINS",
        "http://localhost:3000,http://127.0.0.1:3000",
    ).split(",")
    if o.strip()
]

# ---------------------------------------------------------------------------
# AI provider configuration
# All AI calls are made from backend only — keys are never exposed to frontend.
# Empty AI_API_KEY = AI disabled gracefully (deterministic fallback returned).
# ---------------------------------------------------------------------------
AI_PROVIDER = os.getenv("AI_PROVIDER", "openai")
AI_API_KEY  = os.getenv("AI_API_KEY", "")
AI_MODEL    = os.getenv("AI_MODEL", "gpt-4o-mini")
