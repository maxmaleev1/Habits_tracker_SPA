import os
from datetime import timedelta
from pathlib import Path
from dotenv import load_dotenv


load_dotenv(override=True)

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = True if os.getenv('DEBUG') == 'True' else False

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'drf_yasg',
    'corsheaders',

    'habits',
    'users',
    'telegram_reminder',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",  # Бэкенд PostgreSQL
        "NAME": os.getenv("POSTGRES_DB", "postgres"),  # Название БД
        "USER": os.getenv("POSTGRES_USER", "postgres"),  # Имя пользователя
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "postgres"),  # Пароль
        "HOST": os.getenv("POSTGRES_HOST", "localhost"),  # Адрес хоста БД
        "PORT": os.getenv("POSTGRES_PORT", "5432"),  # Порт PostgreSQL
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

AUTH_USER_MODEL = 'users.User'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = 'users:login'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES':
        ['rest_framework_simplejwt.authentication.JWTAuthentication',],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# URL-адрес брокера сообщений
CELERY_BROKER_URL = os.getenv('LOCATION') # Например, Redis, который по умолчанию работает на порту 6379
# URL-адрес брокера результатов, также Redis
CELERY_RESULT_BACKEND = os.getenv('LOCATION')
# Часовой пояс для работы Celery
CELERY_TIMEZONE = TIME_ZONE
# Флаг отслеживания выполнения задач
CELERY_TASK_TRACK_STARTED = True
# Максимальное время на выполнение задачи
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
CELERY_BEAT_SCHEDULE = {
    'task-name': {
        'task': 'telegram_reminder.tasks.message',
        'schedule': timedelta(minutes=2),
    },
}

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_URL = os.getenv('TELEGRAM_URL')

CORS_ALLOWED_ORIGINS = [
    'https://read-only.example.com',
    'https://read-and-write.example.com',
]
# Для того что бы можно было заходить в админ панель, необходимо указать:
CSRF_TRUSTED_ORIGINS = [
    'https://read-and-write.example.com',
]
# Переменная с флагом False запрещает заходить с других доменов
CORS_ALLOW_ALL_ORIGINS = False

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")