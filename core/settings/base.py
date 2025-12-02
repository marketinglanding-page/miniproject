"""
Django settings for core project.

Common settings for development and production environments.
"""

import os, json
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent # core/settings/base.py 기준이므로 한 단계 더 올라가야 합니다.

# --- Secrets and Environment Loading ---

# SECURITY WARNING: keep the secret key used in production secret!
secret_file = os.path.join(BASE_DIR, "secrets.json")

# 파일을 열고 JSON 로드 시 오류 처리
try:
    with open(secret_file) as f:
        secrets = json.loads(f.read())
except FileNotFoundError:
    print(
        f"Warning: {secret_file} not found. Using environment variables and defaults only."
    )
    secrets = {}
except json.JSONDecodeError:
    raise ImproperlyConfigured(f"Error decoding JSON from {secret_file}")


def get_secret(setting, default=None):
    """환경 변수, JSON 파일, 기본값 순서로 설정을 가져옵니다."""
    # 환경 변수 우선
    if os.environ.get(setting):
        # 환경 변수에서 가져올 때는 문자열 그대로 반환
        return os.environ.get(setting)

    # JSON 파일에서 찾기
    if setting in secrets:
        # JSON에서 가져온 값 반환
        return secrets[setting]

    # 기본값 확인
    if default is not None:
        return default

    # 필수 설정이 없으면 에러 발생
    error_msg = "Set the {} environment variable or define it in secrets.json".format(
        setting
    )
    raise ImproperlyConfigured(error_msg)


# --- Application definition ---

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 서드파티 앱
    "rest_framework",
    "drf_spectacular",
    'rest_framework_simplejwt.token_blacklist',
    # 사용자 정의 앱
    # # 'your_app_name',
    "users.apps.UsersConfig",
    "common.apps.CommonConfig",
    "accounts.apps.AccountsConfig",
    "transactions.apps.TransactionsConfig",
    "analysis.apps.AnalysisConfig",
    "notifications.apps.NotificationsConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

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

WSGI_APPLICATION = "core.wsgi.application"


# --- Password validation ---
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# --- Internationalization ---

LANGUAGE_CODE = "en-us"
TIME_ZONE = get_secret("TIME_ZONE", "Asia/Seoul")
USE_I18N = True
USE_TZ = True


# --- Static files (CSS, JavaScript, Images) ---

STATIC_URL = "static/"
# Django가 수집한 모든 정적 파일이 모이는 최종 경로 (배포 시 Nginx 등 사용)
STATIC_ROOT = BASE_DIR / "staticfiles"
# 개발 시 정적 파일을 찾을 추가 경로
STATICFILES_DIRS = [
    BASE_DIR / "static",
]


# --- Default primary key field type ---
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# --- REST Framework and Spectacular Settings ---
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

# --- drf-spectacular 옵션 ---
SPECTACULAR_SETTINGS = {
    'TITLE': '가계부 API',
    'DESCRIPTION': '가계부 시스템 API 문서',
    'VERSION': 'v1',
}

# 커스텀 User 모델을 사용하도록 지정
AUTH_USER_MODEL = 'users.User'
