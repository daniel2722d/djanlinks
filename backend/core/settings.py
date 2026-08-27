"""
SETTINGS.PY — Configuración central de Django
==============================================

Este archivo controla TODO el comportamiento del backend:
- Apps instaladas, base de datos, idioma, CORS, archivos estáticos.

Las variables sensibles vienen del archivo .env en la raíz del proyecto.
Ver guía: docs/GUIA.md
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Ruta base del backend (carpeta que contiene manage.py)
BASE_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = BASE_DIR.parent
FRONTEND_DIR = ROOT_DIR / 'frontend'

load_dotenv(ROOT_DIR / '.env')

# --- Seguridad (valores en .env) ---
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-change-me-in-production')
DEBUG = os.environ.get('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# --- Apps del proyecto ---
# Django built-in + REST framework + nuestras apps en backend/apps/
INSTALLED_APPS = [
    'django.contrib.admin',       # Panel de administración → /admin/
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',             # API REST para el frontend
    'corsheaders',                # Permite peticiones desde el frontend (otro puerto)
    'apps.users',                 # Usuarios (pendiente)
    'apps.services',              # Catálogo de servicios
    'apps.portfolio',             # Proyectos del portafolio
    'apps.leads',                 # Formularios de contacto
    'apps.ai',                    # Links AI chat
    'apps.dashboard',             # Estadísticas admin
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Debe ir primero
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'  # Rutas principales en core/urls.py

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'core.wsgi.application'

# --- Base de datos PostgreSQL (credenciales en .env) ---
# En local sin Docker: cambia POSTGRES_HOST=localhost en .env
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', 'djanlinks'),
        'USER': os.environ.get('POSTGRES_USER', 'djanlinks'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'djanlinks'),
        'HOST': os.environ.get('POSTGRES_HOST', 'db'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
    }
}

# --- Links AI ---
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
LINKS_WHATSAPP_NUMBER = os.environ.get('LINKS_WHATSAPP_NUMBER', '573052707206')

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'es-co'
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_TZ = True

# Archivos estáticos (CSS/JS del admin) y media (uploads de imágenes)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Orígenes permitidos para peticiones desde el frontend (CORS)
CORS_ALLOWED_ORIGINS = os.environ.get(
    'CORS_ALLOWED_ORIGINS',
    'http://localhost:5500,http://127.0.0.1:5500,http://localhost:3000'
).split(',')

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',  # API pública por ahora
    ],
}
