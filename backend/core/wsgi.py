"""WSGI — Punto de entrada para servidores de producción (Gunicorn, Docker)."""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
application = get_wsgi_application()
