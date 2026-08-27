"""
SERVICES — Catálogo de servicios del estudio
=============================================
Ej: Desarrollo Web, UI/UX, Marketing, IA...
Admin: /admin/ → gestionar desde el panel Django
API:   GET /api/services/
"""
from django.db import models


class Service(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)  # Para URLs: desarrollo-web
    description = models.TextField()
    image = models.ImageField(upload_to='services/', blank=True)
    order = models.PositiveIntegerField(default=0)  # Orden en la página
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'title']

    def __str__(self):
        return self.title
