#!/usr/bin/env python
"""
Punto de entrada del proyecto completo.

Desde la raiz del repositorio puedes ejecutar:
  python manage.py runserver

Django levantara la API y tambien servira el frontend estatico en el mismo
servidor de desarrollo.
"""
import os
import sys
from pathlib import Path


def main():
    root_dir = Path(__file__).resolve().parent
    backend_dir = root_dir / "backend"

    sys.path.insert(0, str(backend_dir))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "No se pudo importar Django. Instala las dependencias con "
            "`pip install -r requirements.txt`."
        ) from exc

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
