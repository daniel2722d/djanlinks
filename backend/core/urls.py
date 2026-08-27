"""
URLS.PY — Mapa de rutas del backend (API)
==========================================

Todas las URLs de la API empiezan con /api/

Ejemplos:
  GET  http://localhost:8000/api/services/     → lista servicios
  GET  http://localhost:8000/api/portfolio/    → lista proyectos
  POST http://localhost:8000/api/leads/        → crear contacto
  POST http://localhost:8000/api/ai/chat/      → chat Links AI
  GET  http://localhost:8000/admin/            → panel Django admin
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .frontend import frontend_asset, frontend_component, frontend_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('apps.users.urls')),           # apps/users/urls.py
    path('api/services/', include('apps.services.urls')),     # apps/services/urls.py
    path('api/portfolio/', include('apps.portfolio.urls')),   # apps/portfolio/urls.py
    path('api/leads/', include('apps.leads.urls')),           # apps/leads/urls.py
    path('api/ai/', include('apps.ai.urls')),                 # apps/ai/urls.py
    path('api/dashboard/', include('apps.dashboard.urls')),   # apps/dashboard/urls.py
    path('assets/<path:path>', frontend_asset),               # CSS/JS/imagenes del frontend
    path('components/<path:path>', frontend_component),       # Navbar, loader, hero, footer
    path('', frontend_page),                                  # Sitio web en /
    path('<str:page>', frontend_page),                        # Paginas HTML exactas
]

# En desarrollo: servir archivos subidos (imágenes de proyectos, etc.)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
