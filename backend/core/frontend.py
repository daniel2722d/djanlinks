"""
Vistas pequenas para servir el frontend estatico desde Django en desarrollo.

Esto permite que `python manage.py runserver` entregue tanto la API como las
paginas HTML, sin un servidor separado para la carpeta frontend/.
"""
from pathlib import Path

from django.conf import settings
from django.http import FileResponse, Http404
from django.utils._os import safe_join


def _frontend_file(relative_path):
    try:
        file_path = Path(safe_join(settings.FRONTEND_DIR, relative_path))
    except ValueError as exc:
        raise Http404("Archivo no encontrado") from exc

    if not file_path.is_file():
        raise Http404("Archivo no encontrado")

    return FileResponse(file_path.open("rb"))


def frontend_page(request, page="index.html"):
    if not page.endswith(".html"):
        raise Http404("Pagina no encontrada")

    return _frontend_file(page)


def frontend_asset(request, path):
    return _frontend_file(f"assets/{path}")


def frontend_component(request, path):
    return _frontend_file(f"components/{path}")
