"""
PORTFOLIO — Proyectos del portafolio (ARQ722, Azul Celeste, etc.)
==================================================================
API: GET /api/portfolio/
Los datos pueden cargarse dinámicamente en portafolio.html en el futuro.
"""
from django.db import models


class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='portfolio/', blank=True)
    tags = models.CharField(max_length=500, blank=True)  # Ej: "Web,UI/UX"
    order = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)  # Mostrar en index
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title
