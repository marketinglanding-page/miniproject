from .base import *

# Quick-start development settings - suitable for development

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_secret("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = get_secret("ALLOWED_HOSTS", ['*'])


# --- Database for Development (Docker Compose or Local) ---
# Docker Compose 환경에서 DB 호스트를 'db' 서비스 이름으로 사용
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": get_secret("DB_NAME", "budget"),
        "USER": get_secret("DB_USER", "budget_admin"),
        "PASSWORD": get_secret("DB_PASSWORD"),
        "HOST": get_secret("DB_HOST", 'localhost'), # Docker Compose 서비스 이름 또는 'localhost'
        "PORT": get_secret("DB_PORT", "5432"),
    }
}