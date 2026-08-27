#!/usr/bin/env python
"""
Punto de entrada Django dentro de backend/.

Uso recomendado desde la raiz del proyecto:
  python manage.py runserver

Este archivo se mantiene por compatibilidad si necesitas ejecutar comandos
desde la carpeta backend/.
"""
import os
import sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
